from random import randint as rnt


"""

Домашнее задание №1

Цикл for: Оценки

* Создать список из словарей с оценками учеников разных классов 
  школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
* Посчитать и вывести средний балл по всей школе.
* Посчитать и вывести средний балл по каждому классу.
"""

def main()-> str:
    school_99 = [{'school_class':'1a',
                  'scores': [rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5)]},
                 
                 {'school_class':'1b',
                  'scores': [rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5)]},
                 
                 {'school_class':'1c',
                  'scores': [rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5),rnt(1,5)]}
                ]
     
    
   
    sum_class_score=0
    sum_school_score=0
    ppl_in_school = 0

    for score in school_99:
        ppl_in_school += len(score['scores'])
        sum_class_score = sum(score['scores']) / len(score['scores'])
        sum_school_score+=sum_class_score / ppl_in_school

        print(f'Средняя оценка по классу: {sum_class_score}')
        print(f'Средняя оценка по школе: {sum_school_score}')
    
if __name__ == "__main__":
    main()
