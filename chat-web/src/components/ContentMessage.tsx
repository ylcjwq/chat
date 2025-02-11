import { marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from "highlight.js";
import "highlight.js/styles/base16/github.css";

export const { createUserContent, createRobotContent } = (() => {
  marked.setOptions({
    highlight: function (code: any, lang: any) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
  } as any);

  marked.use(
    markedHighlight({
      langPrefix: "hljs language-",
      highlight(code, lang) {
        const language = hljs.getLanguage(lang) ? lang : "shell";
        return hljs.highlight(code, { language }).value;
      },
    })
  );

  function _createUserContent(
    username: string,
    content: string,
    content_container: Element
  ) {
    const dom = document.createElement("div");
    dom.className = "user block";
    dom.innerHTML = ` <div class="container">
                    <div class="avatar">
                      ${username}
                    </div>
                    <div class="content markdown-body user">
                      ${_normalizeContent(content)}
                    </div>
                  </div>`;
    const hitBottom = isBottom();
    content_container.appendChild(dom);
    if (hitBottom) {
      document.documentElement.scrollTo(0, 1000000);
    }
  }

  function _normalizeContent(content: string) {
    const processedContent = content
      .replace(/<think>([\s\S]*?)(<\/think>|$)/g, (_, thinkContent, closingTag) => {
        // 当遇到</think>时闭合，否则保持未完成状态
        const isCompleted = !!closingTag;
        // 将思考内容包装到思考容器中，其余内容保持原样
        return _createThinkBlock(
          marked.parse(thinkContent.trim(), { breaks: true, gfm: true }) as string,
          isCompleted
        );
      });
  
    // marked解析处理原始内容（非思考区域的部分）
    const html = marked.parse(processedContent, {
      breaks: true,
      gfm: true,
    });
    return html;
  }
  
  function _createThinkBlock(content: string, isCompleted: boolean) {
    return `</div></div>` + // 结束前一个内容容器
      `<div class="think-container ${isCompleted ? 'completed' : 'thinking'}">` + 
        '<div class="think-header">' +
          `<span class="arrow"></span>${isCompleted ? '思考完成（点击展开）' : '正在思考中...'}` +
        '</div>' +
        `<div class="think-content">${content}</div>` +
      '</div>' +
      '<div>'; // 开启新的内容容器
  }

  function _handleThinkBlocks(container: Element) {
    container.querySelectorAll('.think-container').forEach(think => {
      const header = think.querySelector('.think-header')!;
      const content = think.querySelector('.think-content')! as HTMLElement;
      const isCompleted = think.classList.contains('completed');

      // 初始化显示状态
      content.style.display = isCompleted ? 'none' : 'block';
      think.classList.toggle('expanded', !isCompleted);
  
      // 点击交互逻辑
      header.addEventListener('click', () => {
        think.classList.toggle('expanded');
        content.style.display = think.classList.contains('expanded') ? 'block' : 'none';
      });
    });
  }

  function createUserContent(
    username: string,
    value: string,
    content_container: Element
  ) {
    const content = value.trim();
    _createUserContent(username, content, content_container);
  }

  function _getLastTextNode(dom: any) {
    const children = dom.childNodes;
    for (let i = children.length - 1; i >= 0; i--) {
      const node = children[i];
      if (node.nodeType === Node.TEXT_NODE && /\S/.test(node.nodeValue)) {
        node.nodeValue = node.nodeValue.replace(/\s+$/, "");
        return node;
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        const last: any = _getLastTextNode(node);
        if (last) {
          return last;
        }
      }
    }
    return null;
  }

  function _updateCursor(dom: any) {
    const contentDom = dom;
    const lastText = _getLastTextNode(contentDom);
    const textNode = document.createTextNode("\u200b");
    if (lastText) {
      lastText.parentElement.appendChild(textNode);
    } else {
      contentDom.appendChild(textNode);
    }
    const domRect = contentDom.getBoundingClientRect();
    const range = document.createRange();
    range.setStart(textNode, 0);
    range.setEnd(textNode, 0);
    const rect = range.getBoundingClientRect();
    const x = rect.left - domRect.left;
    const y = rect.top - domRect.top;
    dom.style.setProperty("--x", `${x}px`);
    dom.style.setProperty("--y", `${y}px`);
    textNode.remove();
  }

  function isBottom() {
    return (
      Math.abs(
        document.documentElement.scrollTop +
          document.documentElement.clientHeight -
          document.documentElement.scrollHeight
      ) < 20
    );
  }

  function createRobotContent(content_container: Element) {
    const dom = document.createElement("div");
    dom.className = "robot block typing";
    dom.innerHTML = ` <div class="container">
                  <div class="avatar">
                  <img src="/gptAvatar.svg" alt="" />
                  </div>
                  <div class="content markdown-body robot" style="--x: -1000px; --y: 0px">
                    <div class="thinking-container"></div>
                  </div>
                </div>`;
    const contentDom = dom.querySelector(".content");
    let content = "";
    content_container.appendChild(dom);
    _updateCursor(contentDom);
    function append(text: string) {
      content += text;
      const html = _normalizeContent(content);
      const hitBottom = isBottom();
      contentDom!.innerHTML = html as string;

      // 新增思维块处理
      _handleThinkBlocks(contentDom!);

      if (hitBottom) {
        document.documentElement.scrollTo(0, 1000000);
      }
      _updateCursor(contentDom);
    }

    return {
      append,
      over() {
        dom.classList.remove("typing");
      },
    };
  }

  return {
    createUserContent,
    createRobotContent,
  };
})();
