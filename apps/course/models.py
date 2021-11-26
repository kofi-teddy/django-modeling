from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=20)
    students = models.ManyToManyField(
        Student, related_name="courses", through="Enrollment"
    )

    def __str__(self) -> str:
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_enrollment", fields=["student", "course"]
            )
        ]

    def __str__(self) -> str:
        return f"{self.student} is enrolled in {self.course}"
