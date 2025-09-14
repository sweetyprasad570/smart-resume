#!/usr/bin/env python3
"""
Simple test to verify PDF generation functionality
"""

def test_pdf_imports():
    """Test if required PDF libraries can be imported"""
    try:
        from xhtml2pdf import pisa
        from io import BytesIO
        print("✓ xhtml2pdf import successful")
        
        # Test basic PDF generation
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .header { text-align: center; color: #2c3e50; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Test Resume</h1>
                <p>This is a test PDF generation</p>
            </div>
            <div class="section">
                <h2>Education</h2>
                <p>Bachelor of Computer Science</p>
            </div>
            <div class="section">
                <h2>Skills</h2>
                <p>Python, JavaScript, React, Flask</p>
            </div>
        </body>
        </html>
        """
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("utf-8")), result)
        
        if pdf.err:
            print("✗ PDF generation failed with errors")
            return False
        else:
            print("✓ PDF generation successful")
            print(f"✓ Generated PDF size: {len(result.getvalue())} bytes")
            return True
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ PDF generation error: {e}")
        return False

def test_flask_imports():
    """Test if Flask and related libraries can be imported"""
    try:
        from flask import Flask, jsonify, make_response, render_template_string
        print("✓ Flask imports successful")
        return True
    except ImportError as e:
        print(f"✗ Flask import error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDF and Flask functionality...\n")
    
    flask_ok = test_flask_imports()
    pdf_ok = test_pdf_imports()
    
    print(f"\nResults:")
    print(f"Flask imports: {'✓ OK' if flask_ok else '✗ Failed'}")
    print(f"PDF generation: {'✓ OK' if pdf_ok else '✗ Failed'}")
    
    if flask_ok and pdf_ok:
        print("\n🎉 All tests passed! The download and PDF functionality should work.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
