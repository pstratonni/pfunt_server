from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.permissions import *
from shop.serializers import *
from shop.service import get_client_ip, ProductFilter


class ManufacturerAPIList(generics.ListAPIView):
    queryset = Manufacturer.objects.filter(activ=True)
    serializer_class = ManufacturerSerializer


class ManufacturerAPIRetriever(generics.RetrieveAPIView):
    queryset = Manufacturer.objects.filter(activ=True)
    serializer_class = ManufacturerSerializer


class ManufacturerIsAdminAPIList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (IsAdminUser,)


class ManufacturerIsAdminAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (IsAdminUser,)


class ProductAPIListPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProductAPIList(generics.ListAPIView):
    queryset = Product.objects.filter(active=True).order_by('-date_created')
    serializer_class = ProductListSerializer
    pagination_class = ProductAPIListPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ('title', 'category__title')
    ordering_fields = ('price',)


class ProductAPIRetriever(generics.RetrieveAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductDetailSerializer


class ProductIsAdminAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductAPIListPagination
    permission_classes = (IsAdminUser,)


class ProductIsAdminAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUser,)


class OrderAPIListCreate(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        if user:
            queryset = Order.objects.filter(user=user)
            return queryset
        return Response([])


class OrderIPAPICreate(generics.CreateAPIView):
    serializer_class = OrderIPSerializer


class OrderAPIRetrieve(generics.RetrieveAPIView):
    permission_classes = (IsOwner,)
    queryset = Order.objects.all()
    serializer_class = OrderRetrieveSerializer


class OrderAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)


class OrderItemAPICreate(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = (IsOwnerOrder,)


class OrderItemAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsAdminUser,)


# class CartAuthAPICreate(generics.CreateAPIView, ):
#     serializer_class = CartSerializer
#     permission_classes = (IsAuthenticated,)


class CartAuthAPIRetrieveUpdateDestroy(APIView):
    permission_classes = (IsOwner,)
    # serializer_class = CartSerializer

    def post(self, request):
        if Cart.objects.get(user=request.user):
            return self.get(request)
        else:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(status=400)

    def get(self, request,):
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)

    def put(self, request):
        try:
            instance = Cart.objects.get(user=request.user)
        except:
            return Response({'error': "Object does not exist"})
        serializer = CartSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def delete(self, request):
        try:
            Cart.objects.get(user=request.user).delete()
        except:
           return Response({'error': "Object does not exist"})
        return Response({'delete': "Object has deleted successfully"}, status=204)


class CartIPAPI(APIView):

    def get(self, request):
        try:
            cart = Cart.objects.get(ip=get_client_ip(request))
            return Response(CartIPSerializer(cart).data)
        except:
            pass
        return self.post(request)

    def post(self, request):
        try:
            cart = Cart.objects.get(ip=get_client_ip(request))
            return self.get(request)
        except:
            pass
        serializer = CartIPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(serializer.data, status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        ip = get_client_ip(request)
        try:
            Cart.objects.get(ip=ip).delete()
        except:
           return Response({'error': "Object does not exist"})
        return Response({'delete': "Object has deleted successfully"})

    def put(self, request):
        ip = get_client_ip(request)
        try:
            instance = Cart.objects.get(ip=ip)
        except:
            return Response({'error': "Object does not exist"})
        serializer = CartIPSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartItemAPICreate(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsOwnerCart,)


class CartItemIPAPICreate(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsOwnerCartIP,)


class CartItemAPIUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsOwnerCart,)


class CartItemIPAPIUpdateDestroy(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsOwnerCartIP,)


class PurchaserAPIRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchaser.objects.all()
    serializer_class = PurchaserRetrieveSerializer
    permission_classes = (IsPurchaser,)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.annotate(counting=Count('product', filter=Q(product__active=True), distinct=True))
