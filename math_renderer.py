import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import tempfile

class MathRenderer:
    def __init__(self):
        # Set up matplotlib to use LaTeX for rendering
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def render_math(self, expr: str, fontsize: int = 12) -> str:
        """Render a mathematical expression as an image and return the file path."""
        # Create a figure with minimal margins
        fig = plt.figure(figsize=(10, 0.5))
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)
        ax.axis('off')
        
        # Render the expression
        t = ax.text(0.5, 0.5, f'${expr}$', fontsize=fontsize, 
                   ha='center', va='center', usetex=True)
        
        # Save the figure
        output_path = self.temp_dir / f'math_{abs(hash(expr))}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        
        return str(output_path)
    
    def cleanup(self):
        """Clean up temporary files."""
        for file in self.temp_dir.glob('math_*.png'):
            try:
                file.unlink()
            except OSError:
                pass

# Global instance
math_renderer = MathRenderer()
