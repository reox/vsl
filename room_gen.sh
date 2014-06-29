#!/bin/bash

# generate tex files from a list of room names

while read room
do
    rname=$(echo $room | tr ' /' '_')

cat > rooms/$rname.tex <<EOF
\documentclass[a4paper]{article}
\usepackage{vsl}
\renewcommand\Room{$room}
\begin{document}
\printDoorsign
\end{document}
EOF

done < rooms.txt
