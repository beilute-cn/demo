@echo off
setlocal EnableDelayedExpansion

:menu
cls
echo ============================================
echo  CMD Escape Character Interactive Test
echo ============================================
echo.
echo Select a character to test:
echo.
echo  1. ^^ (Caret)
echo  2. ^& (Ampersand)
echo  3. ^| (Pipe)
echo  4. ^< ^> (Redirects)
echo  5. %% (Percent)
echo  6. " (Quote)
echo  7. ( ) (Parentheses)
echo  8. ! (Exclamation)
echo  9. All Special Characters
echo  0. Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto test_caret
if "%choice%"=="2" goto test_ampersand
if "%choice%"=="3" goto test_pipe
if "%choice%"=="4" goto test_redirect
if "%choice%"=="5" goto test_percent
if "%choice%"=="6" goto test_quote
if "%choice%"=="7" goto test_paren
if "%choice%"=="8" goto test_exclaim
if "%choice%"=="9" goto test_all
if "%choice%"=="0" goto end
goto menu

:test_caret
cls
echo Testing: ^^ (Caret)
echo ==================
echo.
echo Without escape: This is a caret ^
echo This is a caret ^
echo.
echo With escape: This is a caret ^^
echo This is a caret ^^
echo.
pause
goto menu

:test_ampersand
cls
echo Testing: ^& (Ampersand)
echo ======================
echo.
echo Without escape: echo A & echo B
echo A & echo B
echo.
echo With escape: echo A ^^& B
echo A ^& B
echo.
pause
goto menu

:test_pipe
cls
echo Testing: ^| (Pipe)
echo ==================
echo.
echo Without escape: echo hello | findstr hello
echo hello | findstr hello
echo.
echo With escape: echo hello ^^| world
echo hello ^| world
echo.
pause
goto menu

:test_redirect
cls
echo Testing: ^< ^> (Redirects)
echo ==========================
echo.
echo With escape: echo ^^<html^^>^^<body^^>^^</body^^>^^</html^^>
echo ^<html^>^<body^>^</body^>^</html^>
echo.
pause
goto menu

:test_percent
cls
echo Testing: %% (Percent)
echo =====================
echo.
echo With escape: echo 100%%%%
echo 100%%
echo.
pause
goto menu

:test_quote
cls
echo Testing: " (Quote)
echo ===================
echo.
echo With escape: echo ^^"Hello World^^"
echo ^"Hello World^"
echo.
pause
goto menu

:test_paren
cls
echo Testing: ( ) (Parentheses)
echo ===========================
echo.
echo With escape: echo ^^(test^^)
echo ^(test^)
echo.
pause
goto menu

:test_exclaim
cls
echo Testing: ! (Exclamation)
echo ========================
echo.
echo With escape: echo ^^^^!variable^^^^!
echo ^^!variable^^!
echo.
pause
goto menu

:test_all
cls
echo Testing: All Special Characters
echo =================================
echo.
echo ^^  : ^^
echo ^^& : ^&
echo ^^| : ^|
echo ^^< : ^<
echo ^^> : ^>
echo %%%% : %%
echo ^^" : ^"
echo ^^( : ^(
echo ^^) : ^)
echo ^^^^! : ^^!
echo.
pause
goto menu

:end
endlocal
exit /b 0
