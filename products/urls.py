from django.urls import path

from products import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail_view'),
    path("comment<int:product_id>", views.CommentCreateView.as_view(), name='comment-create'),
]
