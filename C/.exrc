if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
inoremap <silent> <S-Tab> =BackwardsSnippet()
imap <silent> <Plug>IMAP_JumpBack =IMAP_Jumpfunc('b', 0)
imap <silent> <Plug>IMAP_JumpForward =IMAP_Jumpfunc('', 0)
inoremap <Plug>ClojureReplDownHistory :call b:vimclojure_repl.downHistory()
inoremap <Plug>ClojureReplUpHistory :call b:vimclojure_repl.upHistory()
inoremap <Plug>ClojureReplEnterHook :call b:vimclojure_repl.enterHook()
inoremap <Nul> 
imap <F5> {}<Up>zzo
imap <F4> {}<Up>zzo
nnoremap  3
map  :py EvaluateCurrentRange()
snoremap <silent> 	 i<Right>=TriggerSnippet()
vmap <NL> <Plug>IMAP_JumpForward
nmap <NL> <Plug>IMAP_JumpForward
noremap  zz
noremap s l
noremap n k
noremap t j
noremap h h
snoremap  b<BS>
nnoremap  3
noremap  S :tabnext
noremap  H :tabprevious
noremap  T :tabnew
noremap  s l
noremap  n k
noremap  t j
noremap  h h
noremap   
noremap    :wa
snoremap % b<BS>%
snoremap ' b<BS>'
nnoremap ' `
map ,t <Plug>TaskList
nmap ,cv:call Screen_Vars()
nmap ,cm ggVG,cc
nmap ,cc vip,cc
vmap ,cc "ry:call Send_to_Screen(@r)
map ,pW :call ShowPyDoc('', 1) 
map ,pw :call ShowPyDoc('', 1) 
nmap <silent> ,lg :LustyBufferGrep
nmap <silent> ,lb :LustyBufferExplorer
nmap <silent> ,lr :LustyFilesystemExplorerFromHere
nmap <silent> ,lf :LustyFilesystemExplorer
nmap ,v :vsplit ~/.vimrc
nmap ,s :source ~/.vimrc
noremap ,h :nohl
noremap ,d !!date +"\%A \%B \%d, \%Y \%r"
nmap ,f :vsplit ~/bqregsysyii/newtest/system/application/files
noremap H ^
noremap J T
noremap K S
noremap L N
noremap N {
noremap Q gqap
noremap S $
noremap T }
snoremap U b<BS>U
snoremap \ b<BS>\
snoremap ^ b<BS>^
snoremap ` b<BS>`
nnoremap ` '
nmap gx <Plug>NetrwBrowseX
noremap j t
noremap k s
noremap l n
noremap n gk
noremap s l
noremap t gj
snoremap <Left> bi
snoremap <Right> a
snoremap <BS> b<BS>
snoremap <silent> <S-Tab> i<Right>=BackwardsSnippet()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#NetrwBrowseX(expand("<cWORD>"),0)
vmap <silent> <Plug>IMAP_JumpBack `<i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpBack "_<Del>i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpForward "_<Del>i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>IMAP_JumpBack i=IMAP_Jumpfunc('b', 0)
nmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
nnoremap <Plug>ClojureCloseResultBuffer :call vimclojure#ResultBuffer.CloseBuffer()
nnoremap <Plug>ClojureStartLocalRepl :call vimclojure#ProtectedPlug(function("vimclojure#StartRepl"), [ b:vimclojure_namespace ])
nnoremap <Plug>ClojureStartRepl :call vimclojure#ProtectedPlug(function("vimclojure#StartRepl"), [  ])
nnoremap <Plug>ClojureEvalParagraph :call vimclojure#ProtectedPlug(function("vimclojure#EvalParagraph"), [  ])
nnoremap <Plug>ClojureEvalToplevel :call vimclojure#ProtectedPlug(function("vimclojure#EvalToplevel"), [  ])
vnoremap <Plug>ClojureEvalBlock :call vimclojure#ProtectedPlug(function("vimclojure#EvalBlock"), [  ])
nnoremap <Plug>ClojureEvalLine :call vimclojure#ProtectedPlug(function("vimclojure#EvalLine"), [  ])
nnoremap <Plug>ClojureEvalFile :call vimclojure#ProtectedPlug(function("vimclojure#EvalFile"), [  ])
nnoremap <Plug>ClojureMacroExpand1 :call vimclojure#ProtectedPlug(function("vimclojure#MacroExpand"), [ 1 ])
nnoremap <Plug>ClojureMacroExpand :call vimclojure#ProtectedPlug(function("vimclojure#MacroExpand"), [ 0 ])
nnoremap <Plug>ClojureRunTests :call vimclojure#ProtectedPlug(function("vimclojure#RunTests"), [ 0 ])
nnoremap <Plug>ClojureRequireFileAll :call vimclojure#ProtectedPlug(function("vimclojure#RequireFile"), [ 1 ])
nnoremap <Plug>ClojureRequireFile :call vimclojure#ProtectedPlug(function("vimclojure#RequireFile"), [ 0 ])
nnoremap <Plug>ClojureGotoSourceInteractive :call vimclojure#ProtectedPlug(function("vimclojure#GotoSource"), [ input("Symbol to go to: ") ])
nnoremap <Plug>ClojureGotoSourceWord :call vimclojure#ProtectedPlug(function("vimclojure#GotoSource"), [ expand("<cword>") ])
nnoremap <Plug>ClojureSourceLookupInteractive :call vimclojure#ProtectedPlug(function("vimclojure#SourceLookup"), [ input("Symbol to look up: ") ])
nnoremap <Plug>ClojureSourceLookupWord :call vimclojure#ProtectedPlug(function("vimclojure#SourceLookup"), [ expand("<cword>") ])
nnoremap <Plug>ClojureMetaLookupInteractive :call vimclojure#ProtectedPlug(function("vimclojure#MetaLookup"), [ input("Symbol to look up: ") ])
nnoremap <Plug>ClojureMetaLookupWord :call vimclojure#ProtectedPlug(function("vimclojure#MetaLookup"), [ expand("<cword>") ])
nnoremap <Plug>ClojureFindDoc :call vimclojure#ProtectedPlug(function("vimclojure#FindDoc"), [  ])
nnoremap <Plug>ClojureJavadocLookupInteractive :call vimclojure#ProtectedPlug(function("vimclojure#JavadocLookup"), [ input("Class to lookup: ") ])
nnoremap <Plug>ClojureJavadocLookupWord :call vimclojure#ProtectedPlug(function("vimclojure#JavadocLookup"), [ expand("<cword>") ])
nnoremap <Plug>ClojureDocLookupInteractive :call vimclojure#ProtectedPlug(function("vimclojure#DocLookup"), [ input("Symbol to look up: ") ])
nnoremap <Plug>ClojureDocLookupWord :call vimclojure#ProtectedPlug(function("vimclojure#DocLookup"), [ expand("<cword>") ])
nnoremap <Plug>ClojureAddToLispWords :call vimclojure#ProtectedPlug(function("vimclojure#AddToLispWords"), [ expand("<cword>") ])
map <silent> <M-Left> :tabprevious
map <silent> <M-Right> :tabnext
map <silent> <C-Right> 
map <silent> <C-Left> 
imap  
inoremap <silent> 	 =TriggerSnippet()
imap <NL> <Plug>IMAP_JumpForward
inoremap <silent> 	 =ShowAvailableSnips()
iabbr pre <pre></pre><Up>
iabbr lth $this->load->helper('');=Eatchar('\s')
iabbr ltl $this->load->library('');=Eatchar('\s')
iabbr ltm $this->load->model('');=Eatchar('\s')
iabbr sw switch (){}<Up>zzf)i=Eatchar('\s')
iabbr fo for (){}<Up>zzf)i=Eatchar('\s')
iabbr wh while (){}<Up>zzf)i=Eatchar('\s')
iabbr iff if (){}<Up>zzf)i=Eatchar('\s')
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set backspace=2
set expandtab
set fileencodings=ucs-bom,utf-8,default,latin1
set guioptions=aegimrLt
set helplang=en
set hidden
set history=200
set hlsearch
set ignorecase
set incsearch
set listchars=trail:~,tab:+-
set mouse=a
set pastetoggle=<F12>
set path=.,/usr/include,,,/usr/local/lib/python2.6/dist-packages/WebError-0.10.1-py2.6.egg,/usr/local/lib/python2.6/dist-packages/Mako-0.2.4-py2.6.egg,/usr/local/lib/python2.6/dist-packages/nose-0.10.4-py2.6.egg,/usr/local/lib/python2.6/dist-packages/decorator-3.0.0-py2.6.egg,/usr/local/lib/python2.6/dist-packages/FormEncode-1.2.1-py2.6.egg,/usr/local/lib/python2.6/dist-packages/PasteScript-1.7.3-py2.6.egg,/usr/local/lib/python2.6/dist-packages/PasteDeploy-1.3.3-py2.6.egg,/usr/local/lib/python2.6/dist-packages/Paste-1.7.2-py2.6.egg,/usr/local/lib/python2.6/dist-packages/Beaker-1.4.1-py2.6.egg,/usr/local/lib/python2.6/dist-packages/WebHelpers-0.6.4-py2.6.egg,/usr/local/lib/python2.6/dist-packages/Routes-1.10.3-py2.6.egg,/usr/local/lib/python2.6/dist-packages/Pylons-0.9.6.2-py2.6.egg,/usr/local/lib/python2.6/dist-packages/QuickWiki-0.1.6-py2.6.egg,/usr/local/lib/python2.6/dist-packages/docutils-0.4-py2.6.egg,/usr/local/lib/python2.6/dist-packages/pymunk-1.0.0-py2.6.egg,/usr/local/lib/python2.6/dist-packages/pip-0.8.2-py2.6.egg,/usr/local/lib/python2.6/dist-packages/South-0.7.3-py2.6.egg,/usr/lib/python2.6,/usr/lib/python2.6/plat-linux2,/usr/lib/python2.6/lib-tk,/usr/lib/python2.6/lib-dynload,/usr/local/lib/python2.6/dist-packages,/usr/lib/python2.6/dist-packages,/usr/lib/python2.6/dist-packages/PIL,/usr/lib/python2.6/dist-packages/gst-0.10,/usr/lib/pymodules/python2.6,/usr/lib/python2.6/dist-packages/gtk-2.0,/usr/lib/pymodules/python2.6/gtk-2.0,/usr/lib/python2.6/dist-packages/wx-2.8-gtk2-unicode
set printoptions=paper:letter
set ruler
set runtimepath=~/.vim,/var/lib/vim/addons,/usr/share/vim/vimfiles,/usr/share/vim/vim72,/usr/share/vim/vimfiles/after,/var/lib/vim/addons/after,~/.vim/after
set scrolloff=3
set shiftwidth=4
set showcmd
set showmatch
set smartindent
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set switchbuf=useopen
set tabstop=4
set tags=./tags,./TAGS,tags,TAGS,~/.vim/tags/python.ctags
set undolevels=200
set whichwrap=h,l,~,[,]
set wildmode=list:longest
" vim: set ft=vim :
