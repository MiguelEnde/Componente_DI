"""
Script para compilar los archivos de traducción .ts a .qm
"""
import os
import subprocess
import sys


def compile_translations():
    """Compila todos los archivos .ts a .qm"""
    translations_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources',
        'translations'
    )
    
    if not os.path.exists(translations_dir):
        print(f"Error: Directory {translations_dir} does not exist")
        return False
    
    # Buscar archivos .ts
    ts_files = [f for f in os.listdir(translations_dir) if f.endswith('.ts')]
    
    if not ts_files:
        print("No .ts files found")
        return False
    
    print(f"Found {len(ts_files)} translation files")
    
    # Compilar cada archivo
    for ts_file in ts_files:
        ts_path = os.path.join(translations_dir, ts_file)
        qm_file = ts_file.replace('.ts', '.qm')
        qm_path = os.path.join(translations_dir, qm_file)
        
        print(f"Compiling {ts_file} -> {qm_file}...")
        
        try:
            # Intentar usar lrelease de PySide6
            result = subprocess.run(
                ['pyside6-lrelease', ts_path, '-qm', qm_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  ✓ Successfully compiled {qm_file}")
            else:
                print(f"  ✗ Error compiling {ts_file}")
                print(f"    {result.stderr}")
        
        except FileNotFoundError:
            print("  ! pyside6-lrelease not found, creating dummy .qm files")
            # Crear archivos .qm vacíos como placeholder
            with open(qm_path, 'wb') as f:
                f.write(b'')
            print(f"  ✓ Created placeholder {qm_file}")
    
    print("\nTranslation compilation complete!")
    return True


if __name__ == "__main__":
    success = compile_translations()
    sys.exit(0 if success else 1)
