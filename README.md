# PolyInPoly
The python code to modify wkt polys. Extend a poly in another poly by a given area

    Interface
  Two polygons are loaded into the lines "Polygon 1" and "Polygon 2", which are connected by several edges, or one polygon completely surrounds the second.
The “Area” line contains the area that needs to be added to polygon 1. The “Simplify” slider allows you to adjust the degree of model simplification, the larger the value, the more angular the polygon will be and the fewer points it will have. 
The line “Output” allows you to select the folder where 2 polygons will be saved. The “Refresh” button refreshes the canvas with the shapes. 
Then there are two large windows, the first window writes everything that the program does and displays the converted first polygon in wkt text format. 
The second window shows the first and second polygon along with the third as a red outline. The first and second windows together allow you to select the result that suits the user.

    Algorithm
  All code is divided into two files. The first file describes the interface and interaction with it (polygon problem). It creates a canvas and takes the data entered by the user. The Functions file (with a very original name) contains all the data processing functions.
  
    First stage, “Optimization” function
  The code translates the text file wkt into a sheet with dots (points are described by sheets of two elements). Then the first polygon is simplified. The program looks for an intersection point with polygon 2, which is surrounded by points (with indices +1 and -1) that also intersect with polygon 2, and checks if the angle is greater than 180 degrees, then the point is deleted. Also the point will be deleted depending on the “Simplify” parameter. A line is built by points with indices +1 and -1 (points must intersect with points of polygon 2) and a buffer is applied to the line, if the point falls into the buffer zone, then it is deleted.
  
    The second stage, creating transformation vectors for intersection points
  After optimization, the program looks for intersection points and creates transformation vectors according to the rules:
Firstly, a vector is created from the midpoint to the intersection point and normalized, if there is no midpoint, then the vector is created from a point that does not intersect with polygon 2 and has an index of +1 or -1. The midpoint between points with indexes +1 and -1 is created provided that these points intersect with second polygon.
Secondly, The vector is multiplied by -1 if the inner rings of the polygon are being edited.
After calling the “InterPoints” function, the output is three sets of data: intersection points (not used in this program), transformation vectors, indexes of intersection points.

    The third stage, the transformation of the polygon and fitting to the desired area
  Transformation vectors are applied indexwise to the points of the polygon using the “PointsXVectors” function. Then the resulting area of ​​the modified polygon is compared with the original one and it is calculated by how much the vector needs to be multiplied to get the desired area ( ref polygon area + user’s desirable area to be added), “ScaleVtoFitA” function. The original polygon is transformed with new vectors by the same function “PointsXVectors”. After such operations, sometimes the polygon becomes incorrect and therefore the “SmartConvex” function is applied. The function applies the convex hull operation only to the intersection points with polygon 2.
After the “SmartConvex” function, the area can change, so the corrected polygon goes through the chain “PointsXVectors”, “ScaleVtoFitA” and “PointsXVectors” again.

    Fourth stage, data output and visualization
  The resulting set of points is converted into a polygon, the resulting area minus the original area is displayed, two polygons are written to a text file and saved in the selected folder. The new polygon is rendered as a canvas outline in the PySimpleGUI window along with the two original polygons.

    Интерфейс
  Загружается два полигона в строки “Polygon 1” и “Polygon 2”, которые соединяются несколькими ребрами или один полигон полностью окружает второй. В строку “Area” записывается площадь, которую нужно прибавить к полигону 1. Слайдер “Simplify” позволяет настроить степень упрощения модели, чем больше значение тем более угловатый будет полигон и тем меньше у него будет точек. Строка “Output” позволяет выбрать папку куда будут сохранены 2 полигона. Кнопка “Refresh” обновляет канвас с изображением фигур. Дальше идет два больших окна, первое окно пишет всё что делает программа и выводит преобразованный первый полигон в текстовом формате wkt. Второе окно показывает первый и второй полигон вместе с третьим в виде красного контура. Первое и второе окно вместе позволяют выбрать результат который устраивает пользователя.
  
    Алгоритм
  Весь код разбит на два файла. Первый файл описывает интерфейс и взаимодействие с ним (poligon problem). В нем создается канвас и и берутся данные введенные пользователем. Файл Functions (с очень оригинальным названием) содержит все функции для обработки данных. 
  
    Первый этап, функция “Optimization”
  Код переводит текстовый файл wkt в лист с точками (точки описываются листами из двух элементов). Затем происходит упрощение первого полигона. Программа ищет точку пересечения с полигоном 2, которая окружена точками (с индексами +1 и -1), которые тоже пересекаются с полигоном 2, и проверяет, если угол больше 180 градусов, то точка удаляется. Также точка будет удалена в зависимости от параметра “Simplify”. Строится линия по точками с индексами +1 и -1 (точки должны пересекаться с точками полигона 2) и применяется buffer к линии, если точка попадает в зону buffer, то она удаляется.
  
    Второй этап, создание векторов трансформации для точек пересечения
  После оптимизации программа ищет точки пересечения и создает вектора трансформации по правилам: 
Во первых, вектор создается от средней точки до точки пересечения и нормализуется, если средней точки нет, то вектор создается от точки, которая не пересекается с полигоном 2 и имеет индекс +1 или -1. Средняя точка между точками с индексами +1 и -1 создается при условии, что эти точки пересекаются с полигоном 2.
Во вторых, вектор умножается на -1 если редактируется внутренние кольца полигона.
После вызова функции “InterPoints” на выходе получается три набора данных: точки пересечения (в данной программе не используются), вектора трансформации, индексы точек пересечения.

    Третий этап, трансформация полигона и подгонка под нужную площадь
  К точкам полигона применяются вектора трансформации по индексно при помощи функции “PointsXVectors”. Затем сравнивается полученная площадь измененного полигона с исходным и вычисляется на сколько нужно умножить вектора, чтобы получить нужную площадь ( ref polygon area + user’s desirable area to be added), функция “ScaleVtoFitA”. Исходный полигон трансформируется уже новыми векторами той жей функцией “PointsXVectors”. После таких операция иногда полигон становится неправильным и поэтому применяется функция “SmartConvex”. Функция применяет операцию convex hull только к точкам пересечения с полигоном 2.
После функции “SmartConvex” площадь может изменится, поэтому исправленный полигон снова проходит через цепочку “PointsXVectors”, “ScaleVtoFitA” и “PointsXVectors”.

    Четвертый этап, вывод данных и визуализация
  Полученный набор точек переводится в полигон выводится полученная площадь минус изначальная площадь, записываются два полигона в текстовый файл и сохраняются в выбранной папке. Новый полигон визуализируется в виде контура в канвас в окне PySimpleGUI вместе с двумя исходными полигонами.
