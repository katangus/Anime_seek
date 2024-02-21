from typing import ValuesView
from django.urls import path
from . import views
# (. significa que importa views da mesma directoria)
app_name = 'anime'
urlpatterns = [
        # anime
        path("", views.anime, name="anime"),
        # anime/3/home
        path("<int:user>/home", views.home, name="home"),
        #anime/login
        path("login", views.loginview, name="loginview"),
        #anime/register
        path("register", views.register, name="register"),
        #anime/add_anime
        path("<int:user>/add_anime", views.add_anime,name="add_anime"),
        #anime/definir_generos
        path("<int:user>/definir_generos", views.definir_generos,name="definir_generos"),
        #anime/3/admin
        path("<int:user>/admin",views.admin,name="admin"),
        #anime/logout
        path("logout", views.logoutview, name="logoutview"),
        #anime/3/personalizar
        path("<int:ide>/personalizar", views.personalizar,name="personalizar"),
        #anime/3/alterar_username
        path("<int:user>/alterar_username", views.alterar_username,name="alterar_username"),
        #anime/3/data
        path("<int:user>/data", views.data,name="data"),
        #anime/3/utilizadores
        path("<int:user>/utilizadores", views.utilizadores,name="utilizadores"),
        #anime/1/3/detail
        path("<int:a>/<int:u>/detail",views.detail,name="detail"),
        #anime/3/4/user
        path("<int:user>/<int:following>/user",views.user,name="user"),
        #anime/3/4/add_user
        path("<int:user>/<int:following>/add_user",views.add_user,name="add_user"),
        #anime/3/4/delete_user_from_list
        path("<int:user>/<int:following>/delete_user_from_list",views.delete_user_from_list,name="delete_user_from_list"),
        #anime/3/4/admin_delete_user
        path("<int:user>/<int:delete>/admin_delete_user",views.admin_delete_user,name="admin_delete_user"),
        #anime/1/3/admin_delete_anime
        path("<int:anime>/<int:user>/admin_delete_anime", views.admin_delete_anime,name="admin_delete_anime"),
        #anime/1/3/delete_anime_from_list
        path("<int:anime>/<int:user>/delete_anime_from_list",views.delete_anime_from_list,name="delete_anime_from_list"),
        #anime/3/import_data
        path("<int:user>/import_data",views.import_data,name="import_data"),
        #anime/3/my_list
        path("<int:user>/my_list",views.my_list,name="my_list"),
        #anime/3/amigos
        path("<int:user>/amigos",views.amigos,name="amigos"),
        #anime/1/3/add_to_list
        path("<int:anime>/<int:user>/add_to_list",views.add_to_list,name="add_to_list"),
        #anime/1/3/todas_reviews
        path("<int:a>/<int:u>/todas_reviews",views.todas_reviews,name="todas_reviews"),
        #anime/3/1/create_reviews
        path("<int:user>/<int:anime>/create_review",views.create_review,name="create_review"),
        #anime/3/erro_imagem
        path("<int:ide>/erro_imagem", views.personalizar, name="erro_imagem"),
        #anime/3/create_otaku_admin
        path("<int:user>/create_otaku_admin",views.create_otaku_admin,name="create_otaku_admin"),


]