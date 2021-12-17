import requests

from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CodeTypeSerializer, PlanSerializer
from .models import User, CodeType, Plan, Codeapply, Code, Plan


class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (SessionAuthentication,BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)


class CreateCodeType(viewsets.ModelViewSet):
    queryset = CodeType.objects.all()
    serializer_class = CodeTypeSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class Plans(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


class UserLogin(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'msg':'Success'
        })


class VouchersApply(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format='json'):
        coupon_code = request.data.get('coupon_code')
        print(coupon_code,"***********")
        if coupon_code:
            try:
                user = User.objects.get(username=request.data.get('username'))
            except User.DoesNotExist:
                user = None
            try:
                code = Code.objects.get(code=coupon_code)
            except Code.DoesNotExist:
                code = None
            
            if not code:
                #check is it a refrral code
                try:
                    check_is_referral =  User.objects.get(referralCode=code)
                except User.DoesNotExist:
                    check_is_referral = None
                if check_is_referral:
                    # check any coupon is used before
                    verify_user = Codeapply.objects.get(userid=user)
                    if verify_user:
                        return Response({'status':status.HTTP_409_CONFLICT ,'msg':'Only valid for the first time purchases..'})
                    else:
                        #first insert coupon data in code table
                        get_code_type = CodeType.objects.get(pk=3)
                        create_newcode = Code.objects.create(
                            codetypeid = get_code_type,
                            code = coupon_code
                        )
                        check_is_referral.askQuestion = check_is_referral.askQuestion+10
                        user.askQuestion = user.askQuestion+20
                        apply_voucher = Codeapply.objects.create(userid=user, codeid=create_newcode)
                        return Response({'status':status.HTTP_200_OK ,'msg':'user and owner user will get 20,10 question extra..'})
                else:
                    telecom_code = requests.get('http://127.0.0.1:8001/telecom/')
                    telecom_res = telecom_code.json()
                    for i in telecom_res:
                        check_telecom_res = coupon_code in i.values()
                        if check_telecom_res:
                            #get codetypee id 4
                            get_code_type = CodeType.objects.get(pk=4)
                            telecom_coupon = list(i.values())[1]
                            #first insert coupon data in code table
                            create_newcode = Code.objects.create(
                                codetypeid = get_code_type,
                                code = coupon_code,
                                amount = list(i.values())[2],
                                status = True
                            )
                            #apply insert data into apply voucher
                            try:
                                verify_user = Codeapply.objects.get(userid=user,codeid=create_newcode)
                            except Codeapply.DoesNotExist:
                                verify_user = None
                            if verify_user:
                                return Response({'status':status.HTTP_409_CONFLICT ,'msg':'Coupon Code cannot be used more than once..'})
                            
                            apply_voucher = Codeapply.objects.create(
                                userid      = user,
                                codeid      = create_newcode
                            )
                            return Response({'status':status.HTTP_200_OK ,'msg':'user will get constant amount of money discount'})
                        
            else:
                #check if code status is active or not
                code_status = code.status
                if code_status:
                    codeplan = code.plan
                    if codeplan:
                        planid = Plan.objects.get(plan_name=codeplan)
                        verify_user = Codeapply.objects.get(userid=user,codeid=code)
                        if verify_user:
                            return Response({'status':status.HTTP_409_CONFLICT ,'msg':'Coupon Code cannot be used more than once..'})
                        apply_voucher = Codeapply.objects.create(
                            userid = user,
                            planid = planid,
                            codeid = code
                        )
                        return Response({'status':status.HTTP_200_OK ,'msg':'user  will get fix discount percentge'})
                    
                    verify_user = Codeapply.objects.filter(userid=user,codeid=code)
                    if verify_user:
                        return Response({'status':status.HTTP_409_CONFLICT ,'msg':'Coupon Code cannot be used more than once..'})
                    apply_voucher = Codeapply.objects.create(
                        userid = user,
                        codeid = code
                    )
                    return Response({'status':status.HTTP_200_OK ,'msg':'user  will get constant amount of money discount'})
                
                return Response({'status':status.HTTP_204_NO_CONTENT ,'msg':'Coupon status is inactive'})
        
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST ,'msg':'Coupon field can not be empty'
        })
