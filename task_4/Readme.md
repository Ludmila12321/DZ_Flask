**Задание**  
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.  
Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.  
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg  
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.  
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.  
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.  

  
  
***task_4_1*** - многопоточный подход,  
***task_4_2*** - многопроцессорный подход,  
***task_4_3*** - асинхронный подход.  

Проверка осуществлялась командами  
python task_4_1.py https://gbcdn.mrgcdn.ru/uploads/post/3175/image/medium-7229ab89c91357205136b32fe224611a.png https://gbcdn.mrgcdn.ru/uploads/avatar/5648406/attachment/thumb-7a4aee493b7863019ffa6660a2dba7e2.jpeg https://gbcdn.mrgcdn.ru/uploads/post/3174/image/medium-c2fd2fa48e63eb668ce5b0699447ca7b.png  
python task_4_2.py https://gbcdn.mrgcdn.ru/uploads/post/3175/image/medium-7229ab89c91357205136b32fe224611a.png https://gbcdn.mrgcdn.ru/uploads/avatar/5648406/attachment/thumb-7a4aee493b7863019ffa6660a2dba7e2.jpeg https://gbcdn.mrgcdn.ru/uploads/post/3174/image/medium-c2fd2fa48e63eb668ce5b0699447ca7b.png  
python task_4_3.py https://gbcdn.mrgcdn.ru/uploads/post/3175/image/medium-7229ab89c91357205136b32fe224611a.png https://gbcdn.mrgcdn.ru/uploads/avatar/5648406/attachment/thumb-7a4aee493b7863019ffa6660a2dba7e2.jpeg https://gbcdn.mrgcdn.ru/uploads/post/3174/image/medium-c2fd2fa48e63eb668ce5b0699447ca7b.png  
Проверить task_4_3 не удалось, так как не ставится пакет aiohttp.