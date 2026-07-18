/**
 * Desmos 图形集成模块
 */
const Graph = {
  instances: {},

  create(containerId, opts = {}) {
    const el = document.getElementById(containerId);
    if (!el || typeof Desmos === 'undefined') return null;

    const calculator = Desmos.calculator(el, {
      keypad: opts.keypad !== false,
      expressions: opts.expressions !== false,
      settingsMenu: false,
      zoomButtons: true,
      expressionsTopbar: opts.topbar !== false,
    });

    this.instances[containerId] = calculator;

    // 设置坐标范围
    if (opts.bounds) {
      calculator.setMathBounds(opts.bounds);
    }

    // 添加预设表达式
    if (opts.expressions) {
      opts.expressions.forEach((expr, i) => {
        calculator.setExpression({ id: `expr-${i}`, latex: expr.latex, color: expr.color || '#c87832' });
      });
    }

    return calculator;
  },

  setExpression(containerId, exprId, latex, color) {
    const calc = this.instances[containerId];
    if (!calc) return;
    calc.setExpression({ id: exprId, latex, color: color || '#c87832' });
  },

  destroy(containerId) {
    const calc = this.instances[containerId];
    if (calc) { calc.destroy(); delete this.instances[containerId]; }
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
