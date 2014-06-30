#!/bin/bash

# generate tex files from a list of room names

while read room
do
    rname=$(echo $room | tr ' /' '_')

cat > rooms/$rname.tex <<EOF
\documentclass[a4paper]{article}
\usepackage{vsl}
\usepackage[top=10mm, bottom=0mm, left=0mm, right=0mm, landscape]{geometry}
\renewcommand\Room{$room}
\begin{document}
\printDoorsign
\end{document}
EOF

done < rooms.txt
