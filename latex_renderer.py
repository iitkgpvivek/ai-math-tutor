import os
import sys
import tempfile
import base64
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image

# Configure matplotlib to use mathtext with DejaVu Sans
mpl.rcParams.update({
    'mathtext.fontset': 'dejavusans',  # Use DejaVu Sans for math text
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 14,
})

class LatexRenderer:
    def __init__(self):
        # Set up temp directory
        self.temp_dir = Path(tempfile.mkdtemp(prefix='math_imgs_'))
        
    def render_inline_math(self, text):
        """Render text with inline math expressions."""
        import re
        from io import BytesIO
        from reportlab.platypus.flowables import Image as ReportLabImage
        
        # Find all math expressions in the text (enclosed in $...$)
        parts = []
        last_end = 0
        
        for match in re.finditer(r'\$([^$]+)\$', text):
            # Add text before the math expression
            if match.start() > last_end:
                parts.append(text[last_end:match.start()])
            
            # Render the math expression
            math_expr = match.group(1)
            try:
                img_path = self.render_latex(math_expr)
                if img_path and os.path.exists(img_path):
                    # Create a ReportLab image flowable
                    img = ReportLabImage(img_path, width=50, height=20)  # Adjust size as needed
                    parts.append(img)
                else:
                    parts.append(f'${math_expr}$')
            except Exception as e:
                print(f"Error rendering math expression: {math_expr}")
                print(f"Error details: {str(e)}")
                parts.append(f'${math_expr}$')
            
            last_end = match.end()
        
        # Add remaining text
        if last_end < len(text):
            parts.append(text[last_end:])
        
        return parts
    
    def render_latex(self, expr):
        """Render a math expression to an image file using matplotlib's mathtext."""
        # Clean and prepare the expression
        expr = expr.strip()
        
        # Convert common LaTeX commands to mathtext format
        expr = self._convert_to_mathtext(expr)
        
        # Create a figure with a tight layout
        fig = plt.figure(figsize=(10, 0.5))
        fig.patch.set_alpha(0.0)  # Transparent background
        
        try:
            # Add text with mathtext rendering
            plt.text(0.5, 0.5, expr,
                   fontsize=16,  # Slightly larger font for better readability
                   ha='center',
                   va='center')
            
            # Remove axes
            plt.axis('off')
            
            # Save the figure to a temporary file
            output_path = self.temp_dir / f'math_{abs(hash(expr))}.png'
            plt.savefig(output_path,
                      dpi=300,
                      bbox_inches='tight',
                      pad_inches=0.1,
                      transparent=True)
            
            return str(output_path)
            
        except Exception as e:
            print(f"Error rendering math expression: {expr}")
            print(f"Error details: {str(e)}")
            
            # Fallback to text representation
            return self._create_fallback_image(expr)
            
        finally:
            # Clean up
            plt.close(fig)
            plt.close('all')
    
    def _convert_to_mathtext(self, expr):
        """Convert common LaTeX commands to matplotlib's mathtext format."""
        # Handle fractions
        import re
        
        # Convert \frac{a}{b} to a/b
        expr = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\1/\2', expr)
        
        # Remove remaining LaTeX commands
        expr = re.sub(r'\\([a-zA-Z]+)', '', expr)
        
        # Remove extra whitespace
        expr = ' '.join(expr.split())
        
        # Ensure it's a math expression
        if not expr.startswith('$'):
            expr = f'${expr}$'
            
        return expr
    
    def _create_fallback_image(self, text):
        """Create a simple image with the text as fallback."""
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Clean up the text
        text = text.replace('$', '').strip()
        
        # Create a white image with some padding
        width, height = 800, 100
        img = Image.new('RGB', (width, height), 'white')
        d = ImageDraw.Draw(img)
        
        # Try different font locations
        font_paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "Arial.ttf"  # Windows/fallback
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 24)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # Draw the text
        d.text((10, 10), text, fill="black", font=font)
        
        # Save the image
        output_path = self.temp_dir / f'fallback_{abs(hash(text))}.png'
        img.save(output_path)
        
        return str(output_path)
    
    def cleanup(self):
        """Clean up temporary files."""
        for file in self.temp_dir.glob('*'):
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

# Clean up on exit
import atexit
atexit.register(latex_renderer.cleanup)
