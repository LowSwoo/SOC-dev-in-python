# Тема № 3. Разработка SoC на языке python 
## Задачи: 
* Проанализировать:
    * Litex(migen)
    * MyHDL
    * PyHDL
* Составить сводную таблицу с плюсами и минусами каждого из инструментов разработки
* Разработать SoC. В составе должны быть: 
   * CPU
   * RAM
   * ROM
   * UART
* Составить отчёт по проделанной работе
---
# Особенности при работе с инструментами
## myHDL
### Установка
Установка myHDL подробно описана на сайте библиотеки  https://www.myhdl.org/start/installation.html
### Ошибки конвертации
При использовании Python версии 3.9.7 на 2.10.2021 (остальные версии Python не были подвержены проверке) существует проблема конвертации исходного кода в verilog или VHDL при использовании массивов.  Проблема была решена изменением содержимого файла _analyze.py
https://github.com/myhdl/myhdl/issues/350#issuecomment-766808788
```python3
diff --git a/myhdl/conversion/_analyze.py b/myhdl/conversion/_analyze.py
index 9ad1111..9adcb08 100644
--- a/myhdl/conversion/_analyze.py
+++ b/myhdl/conversion/_analyze.py
@@ -976,7 +976,10 @@ class _AnalyzeVisitor(ast.NodeVisitor, _ConversionMixin):
     def accessIndex(self, node):
         self.visit(node.value)
         self.access = _access.INPUT
-        self.visit(node.slice.value)
+        if hasattr(node.slice, 'value'):
+            self.visit(node.slice.value)
+        else:
+            self.visit(node.slice)
         if isinstance(node.value.obj, _Ram):
             if isinstance(node.ctx, ast.Store):
                 self.raiseError(node, _error.ListElementAssign)
diff --git a/myhdl/conversion/_toVHDL.py b/myhdl/conversion/_toVHDL.py
index 7942963..f2011b2 100644
--- a/myhdl/conversion/_toVHDL.py
+++ b/myhdl/conversion/_toVHDL.py
@@ -986,7 +986,8 @@ class _ConvertVisitor(ast.NodeVisitor, _ConversionMixin):
         rhs = node.value
         # shortcut for expansion of ROM in case statement
         if isinstance(node.value, ast.Subscript) and \
-                isinstance(node.value.slice, ast.Index) and \
+                (isinstance(node.value.slice, ast.Index) or \
+                 isinstance(node.value.slice, ast.Call)) and \
                 isinstance(node.value.value.obj, _Rom):
             rom = node.value.value.obj.rom
             self.write("case ")
@@ -2391,7 +2392,10 @@ class _AnnotateTypesVisitor(ast.NodeVisitor, _ConversionMixin):
     def accessIndex(self, node):
         self.generic_visit(node)
         node.vhd = vhd_std_logic()  # XXX default
-        node.slice.value.vhd = vhd_int()
+        if hasattr(node.slice, 'value'):
+            node.slice.value.vhd = vhd_int()
+        else:
+            node.slice.vhd = vhd_int()
         obj = node.value.obj
         if isinstance(obj, list):
             assert len(obj)
diff --git a/myhdl/conversion/_toVerilog.py b/myhdl/conversion/_toVerilog.py
index 2f07fc8..060fb15 100644
--- a/myhdl/conversion/_toVerilog.py
+++ b/myhdl/conversion/_toVerilog.py
@@ -749,8 +749,10 @@ class _ConvertVisitor(ast.NodeVisitor, _ConversionMixin):

     def visit_Assign(self, node):
         # shortcut for expansion of ROM in case statement
+        print(f"{type(node.value.slice)}")
         if isinstance(node.value, ast.Subscript) and \
-                isinstance(node.value.slice, ast.Index) and\
+                (isinstance(node.value.slice, ast.Index) or\
+                 isinstance(node.value.slice, ast.Call)) and\
                 isinstance(node.value.value.obj, _Rom):
             rom = node.value.value.obj.rom
 #            self.write("// synthesis parallel_case full_case")

```
###  

---
# Сводная таблица по инструментам разработки

| Характеристика                                                                                                   | Litex (Migen)                               | MyHDL                  | PyHDL                                   |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------- | --------------------------------------- |
| Оффициальная страница                                                                                            | https://github.com/enjoy-digital/litex/wiki | https://www.myhdl.org/ | https://pyhdl.readthedocs.io/en/latest/ |
| Последнее обновление                                                                                             | 1.10.2021                                   | 09.05.2018             | Неизвестно. Предположительно 2016 год   |
| Документация. В оценке используется Субъективная Единица Измерения Николая (СЕИН). Максимальное начение - 100 | 85 СЕИН                                     | 93 СЕИН                | 43 СЕИН                                 |