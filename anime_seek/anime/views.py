from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect,HttpResponseForbidden
from .models import Otaku,Generos,Anime,Friends,Review,List
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
import csv
from django.db.models import Count

# Create your views here.
def anime(request):
    """
    View que abre a página inicial da página web,
    Contém o login e a possibilidade de registar 
    um utilizador
    """
    return render(request, 'anime/anime.html')

@login_required
def home(request,user):
    """
    View que corresponde à página inicial do utilizador:
    Mostra o utilizador, a sua imagem de perfil 
    e ainda o número de utilizadores e animes adicionados 
    à lista do utilizador.
    Adicionalmente, mostra o top 3 de animes adicionados à lista do utilizadores
    """
    u = User.objects.get(id=user)
    try:        
        otaku = Otaku.objects.get(user=u)
    except Otaku.DoesNotExist:
        return HttpResponseRedirect(reverse("anime:create_otaku_admin",args=(user,)))
    friends = Friends.objects.filter(user=user).count()
    lista = List.objects.filter(user=user).count()
    # get top 3 animes in list
    a=List.objects.values("anime").annotate(c=Count('anime_id')).order_by('-c')[:3]
    contador=0
    animes=[]
    for course in a:
        an=course['anime']
        anime=Anime.objects.get(id=an)
        animes.append(anime)
        contador +=1
        if contador==3:
            return render(request, 'anime/home.html',{'user':user,"otaku":otaku,"friends":friends,"animes":lista,'top':animes})
    return render(request, 'anime/home.html',{'user':user,"otaku":otaku,"friends":friends,"animes":lista})

def create_otaku_admin(request,user):
    """
    View que permite que o admin que se registe como otaku, 
    com o intuito de o mesmo ter uma imagem default 
    """
    if request.method == 'POST':
        try:
            birthdate = request.POST.get('birth')
        except KeyError:
            return render(request,"anime/admin_register.html",{"user":user})
        if birthdate:
            u = User.objects.get(id=user)
            ut = Otaku(user=u, birthdate=birthdate,path_image="")
            ut.save()
            print("salvou")
            print(user)
            return HttpResponseRedirect(reverse("anime:home",args=(user,)))
        else:
            return HttpResponseRedirect(reverse("anime:create_otaku_admin",args=(user,)))
    else:
        return render(request, 'anime/admin_register.html',{"user":user})

@login_required
def admin(request,user):
    """
    View que abre o template admin que permite fazer adições à 
    base de dados
    """
    return render(request, 'anime/admin.html',{'user':user})

@login_required
def data(request,user):
    """
    View que abre o template data_base com o intuito de 
    mostrar todos animes registados na base de dados
    """
    anime = Anime.objects.all()
    return render(request,'anime/data_base.html',{'anime': anime, 'user':user})

@login_required
def detail (request,a,u):
    """
    View que abre o template detail com o intuito de mostrar em
    detalhe o anime selecionado pelo utilizador 
    """
    user=User.objects.get(id=u)
    anime = Anime.objects.get(id=a)
    context={"a":anime,"loop":range(0,anime.episodios),"user":user} # loop serve para mostrar os episódios do anime correspondente
    return render (request,"anime/detail.html",context=context)

@login_required
def todas_reviews(request,a,u):
    """
    View que abre o template reviews com o intuito de mostrar 
    todas as reviews feitas ao anime em questão
    """
    anime = Anime.objects.get(id=a)
    review = Review.objects.filter(anime=anime.id).all
    context={"review":review,"user":u,"anime":anime}
    return render (request,"anime/reviews.html",context=context)

@login_required
def my_list(request,user):
    """
    View que abre o template my_list com o intuito de mostrar
    todos os animes adicionados pelo utilizador
    """
    user = User.objects.get(id=user)
    listing = List.objects.filter(user=user.id).all
    context={"list":listing,"user":user}
    return render (request,"anime/my_list.html",context)

def utilizadores(request,user):
    """
    View que abre o template utilizadores com o intuitos de mostrar
    todos os utilizadores registados na base de dados
    """
    utilizadores = User.objects.all()
    return render(request,'anime/utilizadores.html',{'utilizadores': utilizadores, 'user':user})
    
def amigos(request,user):
    """
    View que abre o template amigos com o intuito de mostrar
    todos os utilizadores que o utilizador segue 
    """
    user = User.objects.get(id=user)
    listing = Friends.objects.filter(user=user.id).all
    context={"list":listing,"user":user}
    return render (request,"anime/amigos.html",context)

@login_required
def user(request,user,following):
    """
    View que abre o template user com o intuito de mostrar em 
    detalhe o perfil do utilizador que o user principal vai seguir ou
    deixar de seguir
    """
    user=User.objects.get(id=user)
    following=User.objects.get(id=following)
    o = Otaku.objects.get(id=following.id) 
    friends = Friends.objects.filter(user=following.id).count()
    lista = List.objects.filter(user=following.id).count()
    context={"user":user,"following":following, "image":o.path_image,"friends":friends,"animes":lista,}
    return render (request,"anime/user.html",context=context)

@login_required
def add_user(request,user,following):
    """
    View que permite ao utilizador seguir outro.
    Não é permitido o utilizador seguir-se a si mesmo, pois 
    é redirecionado a uma página de erro
    """
    if request.method == 'POST':
        u = User.objects.get(id=user)
        f = User.objects.get(id=following) 
        if u.id==f.id:
            context = {"add_me":u}
            return render(request, 'anime/error.html',context)
        w,created = Friends.objects.get_or_create(user=u,following=f)
        w.save()
        print('saved')
        return HttpResponseRedirect(reverse("anime:amigos",args=(user,)))
    return render(request, 'anime/user.html',{'user':following})


def loginview(request):
    """
    View que permite fazer o login, redirecionando para a página Home. 
    Por default a imagem é anime/static/anime/images/default.jpg. 
    Caso o utilizador introduza um username ou password errada 
    é direcionado a uma página de erro
    """
    if request.method =='POST':
        try:
            username = request.POST['user']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
        except KeyError:
            return render(request,"anime/anime.html")
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('anime:home',args=(user.id,)))
        else:
            return HttpResponseForbidden('wrong username or password') 
    return render(request,'anime/anime.html',{"user":user})

@login_required
def logoutview(request):
    """ View que permite realizar o logout do utilizador """
    logout(request)
    return HttpResponseRedirect(reverse('anime:anime'))

def register(request):
    """ View que permite fazer o registo de um utilizador.
    Após o registo é direcionado para a página de login."""
    if request.method == 'POST':
        try:
            email = request.POST.get('e-mail')
            username = request.POST.get('username')
            password = request.POST.get('password')
            birthdate = request.POST.get('birthdate')
        except KeyError:
            return render(request,"anime/register.html")
        if email and username and password and birthdate:
            user = User.objects.create_user(email=email, username=username, password=password)
            ident = user.id
            ut = Otaku(user=user, birthdate=birthdate,path_image="")
            ut.save()
            print(' gravou')
            return HttpResponseRedirect(reverse("anime:anime"))
        else:
            return HttpResponseRedirect(reverse("anime:register"))
    else:
        return render(request, 'anime/register.html')

def personalizar(request, ide):
    """ 
    View que permite ao utilizador mudar a sua imagem de perfil, 
    eliminado a antiga
    """
    if request.method == 'POST':
        try:
            myfile = request.FILES['myfile']
        except KeyError:
            return render(request,'anime/personalizar.html', {'ide':ide})
        if myfile:
            fs = FileSystemStorage()
            u = User.objects.get(pk=ide)
            o = Otaku.objects.get(user=u.id)
            name = str(ide)
            file = name + '.jpg'
            teste = Path("anime/static/media/" + file)
            print('cewbic'+ str(myfile))
            if os.path.exists(teste): 
                old_path = 'anime/static/media/'
                os.remove(old_path + file)
                filename = fs.save(file, myfile)
                uploaded_file_url = fs.url(filename)
            else:
                old_path = 'anime/static/media/'
                filename = fs.save(file, myfile)
                uploaded_file_url = fs.url(filename)
            o.path_image = filename
            o.save()       
        return HttpResponseRedirect(reverse('anime:home', args=(ide,)) )
    return render(request, 'anime/personalizar.html', {'ide':ide})

@login_required
def definir_generos(request,user):
    """
    View que permite ao admin adicionar manualmente novos 
    géneros à base de dados
    """
    if request.method == 'POST':
        try:
            genero = request.POST.get('genero')
        except KeyError:
            return render(request,"anime/admin.html")
        if genero:
            g = Generos(genero=genero)
            g.save()
            return HttpResponseRedirect(reverse("anime:admin",args=(user,)))
        else:
            return HttpResponseRedirect(reverse("anime:admin",args=(user,)))
    else:
        return render(request,"anime/admin.html",{"user":user})

@login_required
def add_anime(request,user):
    """
    View que permite ao admin adicionar manualmente um novo
    anime
    """
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            episodios = request.POST.get('episodios')
            genero=request.POST.get('genero')
            logo=request.POST.get('logo')
        except KeyError:
            return render(request,"anime/admin.html")
        if nome and episodios and genero:
            gender,c= Generos.objects.get_or_create(genero=genero)
            a = Anime(anime=nome,episodios=episodios,generos=gender,logo=logo)
            a.save()
            return HttpResponseRedirect(reverse("anime:admin",args=(user,)))
        else:
            return HttpResponseRedirect(reverse("anime:admin",args=(user,)))
    else:
        return render(request,"anime/admin.html",{"user":user})

@login_required
def alterar_username(request,user):
    """
    View que permite ao utilizador alterar o seu username
    """
    if request.method == 'POST':
        try:
            value = request.POST.get('newusername')
        except KeyError: 
            return render(request,"anime/changes.html")
        if value:
            u = User.objects.get(id=user)
            u.username = value
            u.save()
            return HttpResponseRedirect(reverse("anime:home",args=(u.id,)))
        else: 
            return HttpResponseRedirect(reverse("anime:home",args=(user.id,)))
    else:
        return render(request,"anime/changes.html",{"user":user})

def create_review(request,user,anime):
    """
    View que permite ao utilizador criar uma review do
    correspondente anime dentro do template reviews.html
    """
    if request.method == 'POST':
        try:
            review = request.POST.get('review')
        except KeyError: 
            return render(request,"anime/detail.html")
        if review:
            print(user)
            u = User.objects.get(id=user)
            a = Anime.objects.get(id=anime)
            r = Review(user=u,anime=a,comentario=review,pub_data=timezone.now())
            r.save()
            return HttpResponseRedirect(reverse("anime:todas_reviews",args=(anime,user)))
        else: 
            return HttpResponseRedirect(reverse("anime:todas_reviews",args=(anime,user)))
    else:
        return render(request,"anime/detail.html",{"anime":anime})

@login_required
def add_to_list(request,user,anime):
    """
    View que permite ao utilizador adicionar um anime à sua lista 
    """
    if request.method == 'POST':
        u = User.objects.get(id=user)
        a = Anime.objects.get(id=anime)
        w,created = List.objects.get_or_create(user=u, anime=a, watch=True)
        w.save()
        print('saved')
        return HttpResponseRedirect(reverse("anime:my_list",args=(user,)))
    return render(request, 'anime/detail.html',{'user':user},{'anime':anime})

@login_required
def delete_anime_from_list(request,user,anime):
    """
    View que permite que o utilizador remova o anime da sua lista, 
    caso o anime não esteja na lista surge uma página de erro
    """
    if request.method == 'POST':
        u = User.objects.get(id=user)
        a = Anime.objects.get(id=anime)
        try: 
            l = List.objects.get(user=u, anime=a, watch=True)
            l.delete()
            return HttpResponseRedirect(reverse("anime:my_list",args=(user,)))
        except List.DoesNotExist:
            contexto= {"not_add_anime":a}
            return render(request, 'anime/error.html',contexto) 
    return render(request, 'anime/detail.html',{'user':user},{'anime':anime})

def delete_user_from_list(request,user,following):
    """
    View que permite ao utilizador deixar de seguir um utilizador. 
    Caso não siga anteriormente, então surge uma página de erro
    """
    if request.method == 'POST':
        u = User.objects.get(id=user)
        f = User.objects.get(id=following)
        try: 
            l = Friends.objects.get(user=u, following=f)
            l.delete()
            return HttpResponseRedirect(reverse("anime:home",args=(user,)))
        except Friends.DoesNotExist:
            context={"not_add_user":f}
            return render(request, 'anime/error.html',context)
    return render(request, 'anime/user.html',{'user':user},{'following':following})

def admin_delete_anime(request,anime,user):
    """
    View que permite ao admin remover um anime da base de dados 
    """
    if request.method == 'POST':
        a = Anime.objects.get(id=anime)
        a.delete()
        return HttpResponseRedirect(reverse("anime:home",args=(user,)))
    return render(request, 'anime/detail.html',{'user':user},{'anime':anime})

def admin_delete_user(request,user,delete):
    """
    View que permite a eliminação de um utilizador da base de dados
    """
    if request.method == 'POST':
        u = User.objects.get(id=delete)
        u.delete()
        return HttpResponseRedirect(reverse("anime:home",args=(user,)))
    return render(request, 'anime/user.html',{'user':user},{'following':delete})

@login_required
def import_data(request,user):
    """
    View que permite ao admin a importação de um ficheiro csv. 
    O ficheiro deve corresponder às condições que são apresentadas
    no template admin.html
    Nota: Apenas importa 1000 dados
    """
    i=0
    if request.method == 'POST':
        try: 
            file = request.POST.get('file')
        except KeyError: 
            return render(request,"anime/admin.html")
        if file:
            with open(file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if i == 1000:
                        return HttpResponseRedirect(reverse("anime:home",args=(user,)))
                    if row['episodes']== "":
                        episodios=1
                    else:
                        j=0
                        string=""
                        while row['episodes'][j] != ".":
                            string = string + row['episodes'][j]
                            j+=1
                        episodios = int(string)
                    anime=row['title']
                    logo = row['img_url']
                    genre = row['genre']
                    try:
                        Anime.objects.get(anime=anime)
                    except Anime.DoesNotExist:
                        genero,created = Generos.objects.get_or_create(genero=genre)
                        a= Anime(anime=anime,episodios=episodios,generos=genero,logo=logo)
                        a.save()  # appends the wM object to the list     
                        # movie and genres created
                        i+=1
        return HttpResponseRedirect(reverse("anime:home",args=(user,)))
    return render(request, 'anime/admin.html',{'user':user})

