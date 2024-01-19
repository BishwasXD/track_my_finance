from rest_framework import serializers
from accounts.models import User


"""A ModelSerializer automatically defines the serializer field based on model field"""
class UserSerializer(serializers.ModelSerializer):

    """defining custom field for confirm_password as it is not a part of user model"""
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['email','password','confirm_password']
    

    """Adding extra validation step to check two passwords"""
    def validate(self,args):
        password = args.get('password')
        confirm_password = args.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('two password didnot matched')
        return args
    
    """Since we are using custom usermodel, we need to overide the create method provided"""
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']