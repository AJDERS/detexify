# detexify
A script for removing tex-syntax from .tex file(s). `\mathbb{R}` and the like are not removed.

## Usage

<pre><font color="#008700">In [</font><font color="#8AE234"><b>1</b></font><font color="#008700">]: </font><font color="#008700"><b>import</b></font> <font color="#0087D7"><b>detex</b></font>

<font color="#008700">In [</font><font color="#8AE234"><b>2</b></font><font color="#008700">]: </font>tex_text = <font color="#AF5F00">r&quot;\begin</font><font color="#AF5F87"><b>{document}</b></font><font color="#AF5F00"> \begin{align*} f: \mathbb</font><font color="#AF5F87"><b>{R</b></font>
<font color="#008700">   ...: </font><font color="#AF5F87"><b>}</b></font><font color="#AF5F00"> \to \mathbb</font><font color="#AF5F87"><b>{C}</b></font><font color="#AF5F00"> \end{align*} \end</font><font color="#AF5F87"><b>{document}</b></font><font color="#AF5F00">&quot;</font>

<font color="#008700">In [</font><font color="#8AE234"><b>3</b></font><font color="#008700">]: </font>detex.detex(tex_text)
<font color="#870000">Out[</font><font color="#EF2929"><b>3</b></font><font color="#870000">]: </font>&apos; f: \\mathbb{R} \\to \\mathbb{C} &apos;</pre>
