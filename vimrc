""设置= + - * 前后自动空格
""设置,后面自动添加空格
"实现+-*/前后自动添加空格，逗号后面自动添加空格，适用python
"支持+= -+ *= /+格式

function! EqualSign(char)
    if a:char  =~ '='  && getline('.') =~ ".*[(]"
        return a:char
    endif 
    let ex1 = getline('.')[col('.') - 3]
    let ex2 = getline('.')[col('.') - 2]

    if ex1 =~ "[-=+>\/\*]"
        if ex2 !~ "\s"
            return "\<ESC>i".a:char."\<SPACE>"
        else
            return "\<ESC>xa".a:char."\<SPACE>"
        endif 
    else
        if ex2 !~ "\s"
            return "\<SPACE>".a:char."\<SPACE>\<ESC>a"
        else
            return a:char."\<SPACE>\<ESC>a"
        endif 
    endif
endf

"" 自动补全括号，包括大括号
:inoremap ( ()i
:inoremap ) =ClosePair(')')
:inoremap { {}i
:inoremap } =ClosePair('}')
:inoremap [ []i
:inoremap ] =ClosePair(']')
"":inoremap < <>i
:inoremap > =ClosePair('>')

" 在搜索的时候忽略大小写
set ignorecase
set nocompatible
set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]\ %{strftime(\"%d/%m/%y\ -\ %H:%M\")}    

" 带有如下符号的单词不要被换行分割
set iskeyword+=_,$,@,%,#,-
setlocal noswapfile
set noerrorbells

" 状态栏
set laststatus=2
highlight StatusLine cterm=bold ctermfg=yellow ctermbg=blue

autocmd BufReadPost *
 if line("'\"") > 0 && line("'\"") <= line("$") |
   exe "normal! g`\"" |
 endif

" 命令行补全
"set wildmenu
"set backspace=2

set langmenu=zh_CN.UTF-8
language message zh_CN.UTF-8
"set fileencodings=utf-8,GB2312,cp936,gb18030,big5,euc-jp,euc-kr,latin1

set fileencodings=ucs-bom,UTF-8,GBK,BIG5,latin1
set fileencoding=UTF-8
set fileformat=unix
set ambiwidth=double

" 探测文件类型
filetype on
" 为特定文件类型载入相关缩进文件
filetype indent on

set shiftwidth=4
set tabstop=4
set softtabstop=4
set expandtab
set smarttab

""屏蔽鼠标的右键功能
"set mouse=a
set mouse=v
"set list
"set lcs=tab:<+>

"" 高亮字符，让其不受100列限制
:highlight OverLength ctermbg=red ctermfg=white guibg=red guifg=white
:match OverLength '\%101v.*'

"" 总是显示状态行
set laststatus=2
" 
"" 状态行颜色
highlight StatusLine guifg=SlateBlue guibg=Yellow
highlight StatusLine guifg=SlateBlue guibg=White
highlight StatusLineNC guifg=Gray guibg=White
" 

" 设置以缩进的方式自动折叠和设置快捷方式
set foldmethod=indent

set foldlevel=100
set foldopen-=search
set foldopen-=undo
if has("gui_running")

    set lines=25     
    set columns=80   
endif   

set smartcase
set guioptions-=m
set guioptions-=T
set updatecount=0
set ruler
set rulerformat=%20(%2*%<%f%=\ %m%r\ %3l\ %c\ %p%%%)
set backspace=2
set cursorline              "开启横行#set cursorcolumn            "开启竖行
"""set number
syntax on

map <F11> :! python -i % <CR>

map <F4> ms:call TitleDet()<cr>'s
function AddTitle()
    call append(0,"#!/usr/bin/env python")
    call append(1,"# coding=utf8")
    call append(2,"# Filename: ".expand("%:t"))
    call append(3,"# Last modified: ".strftime("%Y-%m-%d %H:%M"))
    call append(4,"# Author: itnihao")
    call append(5,"# Mail: itnihao@qq.com")
    call append(6,"# Description: ")
    call append(7,"")
    echohl WarningMsg | echo "Successful in adding the copyright." | echohl None
endf


function TitleDet()
    let n=1
    "默认为添加
    while n < 10
        let line = getline(n)
        if line =~ '^\#\s*\S*Last\smodified:\S*.*$'
            call UpdateTitle()
            return
        endif
        let n = n + 1
    endwhile
    call AddTitle()
endfunction

set autochdir "自动获得当前路径

""设置= + - * 前后自动空格
"设置,后面自动添加空格
au FileType python inoremap <buffer>= <c-r>=EqualSign('=')<CR> 
au FileType python inoremap <buffer>+ <c-r>=EqualSign('+')<CR>
au FileType python inoremap <buffer>- <c-r>=EqualSign('-')<CR>
au FileType python inoremap <buffer>* <c-r>=EqualSign('*')<CR>
"au FileType python inoremap <buffer>/ <c-r>=EqualSign('/')<CR>
""au FileType python inoremap <buffer>> <c-r>=EqualSign('>')<CR>
""au FileType python inoremap <buffer>< <c-r>=EqualSign('<')<CR>
au FileType python inoremap <buffer>: <c-r>=Swap()<CR>
au FileType python inoremap <buffer>, ,<space>

function Swap() 
    if getline('.')[col('.') - 1] =~ ")"    
        return "\<ESC>la:"                  
    else                                    
        return ":"                          
    endif                                   
endf


function! ClosePair(char)
    if getline('.')[col('.') - 1] == a:char
        return "\<Right>"
    else
        return a:char
    endif
endf


"设置( { [ < 自动配对
:inoremap ( ()<ESC>i
:inoremap ) <c-r>=ClosePair(')')<CR>
:inoremap { {}<ESC>i
:inoremap } <c-r>=ClosePair('}')<CR>
:inoremap [ []<ESC>i
:inoremap ] <c-r>=ClosePair(']')<CR>
:inoremap < <><ESC>i
:inoremap > <c-r>=ClosePair('>')<CR>
