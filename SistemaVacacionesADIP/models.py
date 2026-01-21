from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class Area(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    area_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subareas'
    )

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def clean(self):
        if self.area_padre:
            if self.area_padre == self:
                raise ValidationError("Un area no puede ser su propia area")
            if not self.area_padre.activo:
                raise ValidationError("El area padre debe ser activo")

    def __str__(self):
        return self.nombre

class Celula(models.Model):
    nombre = models.CharField(max_length=200)

    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='celulas'
    )

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'celula'
        verbose_name = 'Celula'
        verbose_name_plural = 'Celulas'
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'area'],
                name='unique_celula_por_area'
            )
        ]

    def clean(self):
        if not self.area.activo:
            raise ValidationError("No se puede asignar una celula a una area activa")

    def __str__(self):
        return self.nombre

class Puesto(models.Model):
    nombre = models.CharField(max_length=200)
    nivel = models.PositiveIntegerField()

    puesto_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subpuestos'
    )

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'puesto'
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'
        ordering = ['nivel']

    def __str__(self):
        return f"{self.nombre} (Nivel {self.nivel})"

    def clean(self):
        if self.puesto_padre:
            if self.puesto_padre == self:
                raise ValidationError("Un puesto no puede ser su propio padre")
            if self.puesto_padre.nivel >= self.nivel:
                raise ValidationError(
                    "El puesto padre debe tener un nivel jerarquico menor"
                )

class Empleado(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='empleado'
    )

    tipo_contrato = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='empleados'
    )

    puesto = models.ForeignKey(
        Puesto,
        on_delete=models.PROTECT,
        related_name='empleados'
    )

    celula = models.ForeignKey(
        Celula,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empleados'
    )

    jefe_directo = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'subordinados'
    )

    fecha_ingreso = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username}"

    def clean(self):
        errors = {}

        if not self.area.activo:
            errors['area'] = 'El area debe estar activa'

        if not self.puesto.activo:
            errors['puesto'] = 'El puesto debe estar activo.'

        if self.celula:
            if not self.celula.activo:
                errors['celula'] = 'La celula debe estar activa'
            if self.celula.area != self.area:
                errors['celula'] = "La celula no pertenece al area asignada"

        if self.jefe_directo:
            if self.jefe_directo == self:
                errors['jefe_directo'] = 'Un empleado no puede ser su propio jefe'
            if self.jefe_directo.puesto.nivel >= self.puesto.nivel:
                errors['jefe_directo'] = (
                    "El jefe directo debe tener un nivel jerarquico mayor."
                )

        if self.fecha_baja and self.fecha_baja < self.fecha_ingreso:
            errors['fecha_baja'] = (
                "La fecha de baja no puede ser anterior a la fecha de ingreso"
            )

        if errors:
            raise ValidationError(errors)