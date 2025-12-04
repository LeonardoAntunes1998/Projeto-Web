from django.db import models

class Bloco(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Torre(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="torres")
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.bloco.nome}"

class Apartamento(models.Model):
    torre = models.ForeignKey(Torre, on_delete=models.CASCADE, related_name="apartamentos")
    numero = models.CharField(max_length=20)

    def __str__(self):
        return f"Apto {self.numero} - {self.torre.nome} - {self.torre.bloco.nome}"