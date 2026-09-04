from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        ##these are the fields of our registation api accepts

        fields=["email","password","first_name","last_name"]
        #means that client can send the password but we never return an API RESPONSE

        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self,validated_data):
        user=User(
            email=validated_data["email"],
            first_name=validated_data.get("first_name",""),
            last_name=validated_data.get("last_name",""),
        )
        user.set_password(validated_data["password"])

        user.save()

        return user