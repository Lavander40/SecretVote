# SecretVote
'''plantuml
@startuml

class Расписание {
  -classList: list
  +setClassList(list)
}

class Декан {
  +sign(schedule)
}

class Институт {

}

class Пара {
  -teacher
  -group
}

class Преподаватель {
  -speciality
  +getBusiness(day, numberOfClass): bool
  +getSpeciality(): speciality
}

class Кафедра {

}

class Группа {
  -teacher
  +setTeacher(teacher)
}

class Курс {

}

class Занятие {

}

class Дисциплина {
  -speciality
}

class Студент {

}

class Материал {

}

Расписание <-down- Декан: утвержает
Декан -> Институт: руководит
Институт o- Кафедра: относится к
Преподаватель -> Кафедра: работает на
Пара <- Преподаватель: проводит
Расписание -up-* Пара
Дисциплина -* Кафедра: состоит из
Материал <-up- Дисциплина: разрабатывает
Материал -down-* Занятие: читается на
Занятие -> Пара: проводится на
Курс -> Дисциплина
Группа -o Курс: относится к
Студент -up-* Группа: относится к

@enduml
