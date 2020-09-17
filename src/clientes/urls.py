from .views import persons_list, persons_new, persons_update, persons_delete, \
    PersonList, PersonDetail, PersonCreate, ProdutoBulk, PersonUpdate, PersonDelete
from django.urls import path


urlpatterns = [
    path('list/', persons_list, name="person_list"),
    path('new/', persons_new, name="person_new"),
    path('update/<int:id>/', persons_update, name="persons_update"),
    path('delete/<int:id>/', persons_delete, name="persons_delete"),
    path('person_list/', PersonList.as_view(), name='person_list_cbv'),
    path('person_detail/<int:pk>/', PersonDetail.as_view(), name='person_detail_cbv'),
    path('person_update/<int:pk>/', PersonUpdate.as_view(), name='person_update_cbv'),
    path('person_delete/<int:pk>/', PersonDelete.as_view(), name='person_delete_cbv'),
    path('person_create/', PersonCreate.as_view(), name='person_create_cbv'),
    path('person_bulk/', ProdutoBulk.as_view(), name='person_bulk'),
]
