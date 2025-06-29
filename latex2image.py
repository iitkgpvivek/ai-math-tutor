import os
import sys
from pathlib import Path
import matplotlib as mpl
mpl.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

class LatexRenderer:
    def __init__(self):
        self.temp_dir = Path("temp_math")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Configure matplotlib for LaTeX rendering
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman"],
            "font.size": 12,
            "text.latex.preamble": r"""
                \usepackage{amsmath}
                \usepackage{amssymb}
                \usepackage{amsfonts}
                \usepackage{bm}
            """
        })
    
    def render_latex(self, expr: str, dpi: int = 300) -> str:
        """Render a LaTeX expression to an image file."""
        # Create a figure with minimal margins
        fig = plt.figure(figsize=(6, 0.5))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        # Render the expression
        t = ax.text(0.5, 0.5, f'${expr}$', 
                   horizontalalignment='center',
                   verticalalignment='center',
                   transform=ax.transAxes,
                   fontsize=12)
        
        # Save the figure
        output_path = self.temp_dir / f'math_{abs(hash(expr))}.png'
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        
        return str(output_path)
    
    def cleanup(self):
        """Clean up temporary files."""
        for file in self.temp_dir.glob('math_*.png'):
            try:
                file.unlink()
            except OSError:
                pass
        try:
            self.temp_dir.rmdir()
        except OSError:
            pass

# Global instance
latex_renderer = LatexRenderer()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        print(latex_renderer.render_latex(expr))
    else:
        print("Please provide a LaTeX expression to render.")
