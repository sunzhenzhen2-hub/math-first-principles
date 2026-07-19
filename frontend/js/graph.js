/**
 * 自定义 SVG 图形渲染模块 — 无外部依赖
 */
const Graph = {
  instances: {},

  create(containerId, opts = {}) {
    const el = document.getElementById(containerId);
    if (!el) {
      console.warn(`[Graph] Container not found: ${containerId}`);
      return null;
    }

    try {
      console.log(`[Graph] Creating SVG graph in ${containerId}`);

      // 清空容器
      el.innerHTML = '';

      const bounds = opts.bounds || { left: -10, right: 10, bottom: -10, top: 10 };
      const width = el.clientWidth || 600;
      const height = el.clientHeight || 360;

      // 创建 SVG
      const svg = this._createSVG(el, width, height, bounds);

      // 绘制坐标轴
      this._drawAxes(svg, width, height, bounds);

      // 绘制表达式
      if (opts.expressions) {
        opts.expressions.forEach((expr, i) => {
          this._drawExpression(svg, expr, width, height, bounds);
        });
      }

      this.instances[containerId] = { svg, bounds, width, height, element: el };

      console.log(`[Graph] SVG graph created successfully in ${containerId}`);
      return true;
    } catch (e) {
      console.error(`[Graph] Failed to create graph: ${e.message}`);
      return null;
    }
  },

  _createSVG(container, width, height, bounds) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', height);
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.style.background = '#faf6f0';
    svg.style.borderRadius = '12px';
    container.appendChild(svg);
    return svg;
  },

  _toScreen(x, y, width, height, bounds) {
    const xRange = bounds.right - bounds.left;
    const yRange = bounds.top - bounds.bottom;
    const screenX = ((x - bounds.left) / xRange) * width;
    const screenY = height - ((y - bounds.bottom) / yRange) * height;
    return { x: screenX, y: screenY };
  },

  _drawAxes(svg, width, height, bounds) {
    const origin = this._toScreen(0, 0, width, height, bounds);

    // X轴
    if (origin.y >= 0 && origin.y <= height) {
      const xAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      xAxis.setAttribute('x1', 0);
      xAxis.setAttribute('y1', origin.y);
      xAxis.setAttribute('x2', width);
      xAxis.setAttribute('y2', origin.y);
      xAxis.setAttribute('stroke', '#888');
      xAxis.setAttribute('stroke-width', '1');
      xAxis.setAttribute('stroke-dasharray', '4,4');
      svg.appendChild(xAxis);
    }

    // Y轴
    if (origin.x >= 0 && origin.x <= width) {
      const yAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      yAxis.setAttribute('x1', origin.x);
      yAxis.setAttribute('y1', 0);
      yAxis.setAttribute('x2', origin.x);
      yAxis.setAttribute('y2', height);
      yAxis.setAttribute('stroke', '#888');
      yAxis.setAttribute('stroke-width', '1');
      yAxis.setAttribute('stroke-dasharray', '4,4');
      svg.appendChild(yAxis);
    }

    // 绘制刻度
    const xStep = this._calcStep(bounds.right - bounds.left);
    const yStep = this._calcStep(bounds.top - bounds.bottom);

    for (let x = Math.ceil(bounds.left); x <= bounds.right; x += xStep) {
      if (x === 0) continue;
      const pos = this._toScreen(x, 0, width, height, bounds);
      if (pos.y >= 0 && pos.y <= height) {
        const tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        tick.setAttribute('x1', pos.x);
        tick.setAttribute('y1', pos.y - 3);
        tick.setAttribute('x2', pos.x);
        tick.setAttribute('y2', pos.y + 3);
        tick.setAttribute('stroke', '#666');
        tick.setAttribute('stroke-width', '1');
        svg.appendChild(tick);

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', pos.x);
        label.setAttribute('y', pos.y + 15);
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('font-size', '10');
        label.setAttribute('fill', '#666');
        label.textContent = x;
        svg.appendChild(label);
      }
    }

    for (let y = Math.ceil(bounds.bottom); y <= bounds.top; y += yStep) {
      if (y === 0) continue;
      const pos = this._toScreen(0, y, width, height, bounds);
      if (pos.x >= 0 && pos.x <= width) {
        const tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        tick.setAttribute('x1', pos.x - 3);
        tick.setAttribute('y1', pos.y);
        tick.setAttribute('x2', pos.x + 3);
        tick.setAttribute('y2', pos.y);
        tick.setAttribute('stroke', '#666');
        tick.setAttribute('stroke-width', '1');
        svg.appendChild(tick);

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', pos.x - 10);
        label.setAttribute('y', pos.y + 4);
        label.setAttribute('text-anchor', 'end');
        label.setAttribute('font-size', '10');
        label.setAttribute('fill', '#666');
        label.textContent = y;
        svg.appendChild(label);
      }
    }
  },

  _calcStep(range) {
    if (range <= 5) return 1;
    if (range <= 10) return 2;
    if (range <= 20) return 5;
    return 10;
  },

  _drawExpression(svg, expr, width, height, bounds) {
    const latex = expr.latex;
    const color = expr.color || '#c87832';
    const lineWidth = parseFloat(expr.lineWidth) || 2.5;
    const isDashed = expr.lineStyle === 'DASHED';
    const pointStyle = expr.pointStyle || 'NONE';
    const pointSize = parseFloat(expr.pointSize) || 9;
    const label = expr.label || '';

    // 解析点 (x,y)
    const pointMatch = latex.match(/^\(([^,]+),([^)]+)\)$/);
    if (pointMatch) {
      const x = parseFloat(pointMatch[1]);
      const y = parseFloat(pointMatch[2]);
      const pos = this._toScreen(x, y, width, height, bounds);

      if (pointStyle === 'POINT') {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', pos.x);
        circle.setAttribute('cy', pos.y);
        circle.setAttribute('r', pointSize / 2);
        circle.setAttribute('fill', color);
        svg.appendChild(circle);

        if (label) {
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', pos.x + pointSize);
          text.setAttribute('y', pos.y + 4);
          text.setAttribute('font-size', '11');
          text.setAttribute('fill', color);
          text.setAttribute('font-weight', '600');
          text.textContent = label;
          svg.appendChild(text);
        }
      }
      return;
    }

    // 解析水平线 y=c
    const hLineMatch = latex.match(/^y=([^\\{]+)(?:\\left\{.*)?$/);
    if (hLineMatch) {
      const y = parseFloat(hLineMatch[1]);
      if (!isNaN(y)) {
        const pos1 = this._toScreen(bounds.left, y, width, height, bounds);
        const pos2 = this._toScreen(bounds.right, y, width, height, bounds);
        this._drawLine(svg, pos1.x, pos1.y, pos2.x, pos2.y, color, lineWidth, isDashed);

        if (label) {
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', width - 5);
          text.setAttribute('y', pos1.y - 5);
          text.setAttribute('text-anchor', 'end');
          text.setAttribute('font-size', '11');
          text.setAttribute('fill', color);
          text.textContent = label;
          svg.appendChild(text);
        }
      }
      return;
    }

    // 解析垂直线 x=c
    const vLineMatch = latex.match(/^x=([^\\{]+)(?:\\left\{.*)?$/);
    if (vLineMatch) {
      const x = parseFloat(vLineMatch[1]);
      if (!isNaN(x)) {
        const pos1 = this._toScreen(x, bounds.bottom, width, height, bounds);
        const pos2 = this._toScreen(x, bounds.top, width, height, bounds);
        this._drawLine(svg, pos1.x, pos1.y, pos2.x, pos2.y, color, lineWidth, isDashed);

        if (label) {
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', pos1.x + 5);
          text.setAttribute('y', 15);
          text.setAttribute('font-size', '11');
          text.setAttribute('fill', color);
          text.textContent = label;
          svg.appendChild(text);
        }
      }
      return;
    }

    // 解析函数 y=f(x)
    const funcMatch = latex.match(/^y=(.+?)(?:\\left\{.*)?$/);
    if (funcMatch) {
      const funcLatex = funcMatch[1];
      const func = this._parseLatexFunction(funcLatex);
      if (func) {
        this._drawFunction(svg, func, width, height, bounds, color, lineWidth, isDashed, label);
      }
    }
  },

  _drawLine(svg, x1, y1, x2, y2, color, width, dashed) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', color);
    line.setAttribute('stroke-width', width);
    if (dashed) line.setAttribute('stroke-dasharray', '8,4');
    svg.appendChild(line);
  },

  _parseLatexFunction(latex) {
    // 简化的 LaTeX 函数解析器
    // 支持: x^2, 2x, x+1, sin(x), cos(x), e^x, ln(x), 1/2^x 等

    // 替换常见 LaTeX 函数
    let jsExpr = latex
      .replace(/\\sin\(/g, 'Math.sin(')
      .replace(/\\cos\(/g, 'Math.cos(')
      .replace(/\\tan\(/g, 'Math.tan(')
      .replace(/\\ln\(/g, 'Math.log(')
      .replace(/\\log\(/g, 'Math.log10(')
      .replace(/\\sqrt\(/g, 'Math.sqrt(')
      .replace(/\\pi/g, 'Math.PI')
      .replace(/\\e(?![a-z])/g, 'Math.E')
      .replace(/\^/g, '**');

    // 尝试创建函数
    try {
      return new Function('x', `return ${jsExpr};`);
    } catch (e) {
      console.warn(`[Graph] Failed to parse function: ${latex}`);
      return null;
    }
  },

  _drawFunction(svg, func, width, height, bounds, color, lineWidth, dashed, label) {
    const points = [];
    const steps = 200;
    const xRange = bounds.right - bounds.left;

    for (let i = 0; i <= steps; i++) {
      const x = bounds.left + (i / steps) * xRange;
      try {
        const y = func(x);
        if (isFinite(y) && y >= bounds.bottom - 1 && y <= bounds.top + 1) {
          const pos = this._toScreen(x, y, width, height, bounds);
          points.push(pos);
        } else {
          points.push(null);
        }
      } catch (e) {
        points.push(null);
      }
    }

    // 绘制曲线
    let pathData = '';
    let started = false;

    points.forEach((p, i) => {
      if (p) {
        if (!started) {
          pathData += `M ${p.x} ${p.y}`;
          started = true;
        } else {
          pathData += ` L ${p.x} ${p.y}`;
        }
      } else {
        started = false;
      }
    });

    if (pathData) {
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', pathData);
      path.setAttribute('stroke', color);
      path.setAttribute('stroke-width', lineWidth);
      path.setAttribute('fill', 'none');
      if (dashed) path.setAttribute('stroke-dasharray', '8,4');
      svg.appendChild(path);

      if (label) {
        // 在曲线末端添加标签
        const lastPoint = points.filter(p => p).pop();
        if (lastPoint) {
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', lastPoint.x + 5);
          text.setAttribute('y', lastPoint.y - 5);
          text.setAttribute('font-size', '11');
          text.setAttribute('fill', color);
          text.setAttribute('font-weight', '600');
          text.textContent = label;
          svg.appendChild(text);
        }
      }
    }
  },

  destroy(containerId) {
    const instance = this.instances[containerId];
    if (instance) {
      // 清空 SVG 内容
      if (instance.svg && instance.svg.parentNode) {
        instance.svg.parentNode.removeChild(instance.svg);
      }
      delete this.instances[containerId];
    }
  },

  destroyAll() {
    Object.keys(this.instances).forEach(id => this.destroy(id));
  },

  // 常用函数图形配置
  presets: {
    quadratic: { latex: 'y=x^2', bounds: { left: -5, right: 5, bottom: -2, top: 10 } },
    linear: { latex: 'y=2x+1', bounds: { left: -5, right: 5, bottom: -5, top: 10 } },
    sine: { latex: 'y=\\sin(x)', bounds: { left: -7, right: 7, bottom: -2, top: 2 } },
    exponential: { latex: 'y=2^x', bounds: { left: -5, right: 5, bottom: -1, top: 10 } },
    logarithm: { latex: 'y=\\ln(x)', bounds: { left: -1, right: 8, bottom: -4, top: 4 } },
    cube: { latex: 'y=x^3', bounds: { left: -4, right: 4, bottom: -10, top: 10 } },
  }
};
