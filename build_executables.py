"""
Script para crear ejecutables del proyecto con PyInstaller
"""
import os
import subprocess
import sys


def create_executable(script_name, exe_name, icon=None):
    """Crea un ejecutable usando PyInstaller"""
    
    print(f"\n{'='*60}")
    print(f"Creating executable: {exe_name}")
    print(f"{'='*60}\n")
    
    # Comando base de PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',           # Un solo archivo ejecutable
        '--windowed',          # Sin consola (para aplicaciones GUI)
        f'--name={exe_name}',  # Nombre del ejecutable
        '--clean',             # Limpiar caché
    ]
    
    # Añadir datos adicionales
    cmd.extend([
        '--add-data', f'ui_files{os.pathsep}ui_files',
        '--add-data', f'resources{os.pathsep}resources',
        '--add-data', f'models{os.pathsep}models',
        '--add-data', f'views{os.pathsep}views',
        '--add-data', f'controllers{os.pathsep}controllers',
    ])
    
    # Añadir icono si se proporciona
    if icon and os.path.exists(icon):
        cmd.extend(['--icon', icon])
    
    # Añadir el script
    cmd.append(script_name)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"\n Successfully created {exe_name}.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n Error creating {exe_name}.exe")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("\n PyInstaller not found. Please install it with: pip install pyinstaller")
        return False


def main():
    """Función principal"""
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('main.py'):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    print("="*60)
    print("DIGITAL CLOCK PROJECT - EXECUTABLE BUILDER")
    print("="*60)
    
    # Verificar PyInstaller
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except FileNotFoundError:
        print("\nPyInstaller is not installed.")
        print("Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
            print("✓ PyInstaller installed successfully")
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            print("Please install manually: pip install pyinstaller")
            sys.exit(1)
    
    success_count = 0
    total_count = 1
    
    # Crear ejecutable de la aplicación principal
    if create_executable('main.py', 'RelojDigital'):
        success_count += 1
    
    # Resumen
    print("\n" + "="*60)
    print(f"BUILD SUMMARY: {success_count}/{total_count} executables created successfully")
    print("="*60)
    
    if success_count == total_count:
        print("\n✓ All executables created successfully!")
        print("\nYou can find it in the 'dist' folder:")
        print("  - dist/RelojDigital.exe")
    else:
        print("\n⚠ Some executables failed to build")
        print("Please check the error messages above")
    
    # Limpiar archivos temporales
    print("\nCleaning up temporary files...")
    for folder in ['build', '__pycache__']:
        if os.path.exists(folder):
            import shutil
            try:
                shutil.rmtree(folder)
                print(f"   Removed {folder}")
            except Exception as e:
                print(f"   Could not remove {folder}: {e}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
