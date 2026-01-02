"""
Simple script to test camera access
Run this to verify your camera is working before using the main application
"""
import cv2
import sys

def test_camera():
    print("Testing camera access...")
    print("=" * 50)
    
    # Try different camera indices
    for camera_index in range(3):
        print(f"\nTrying camera index {camera_index}...")
        
        # On Windows, try DirectShow backend
        if sys.platform == 'win32':
            backends = [
                (cv2.CAP_DSHOW, "DirectShow"),
                (cv2.CAP_ANY, "Default")
            ]
        else:
            backends = [(cv2.CAP_ANY, "Default")]
        
        for backend, backend_name in backends:
            try:
                print(f"  Trying {backend_name} backend...")
                cap = cv2.VideoCapture(camera_index, backend)
                
                if not cap.isOpened():
                    print(f"  ❌ Camera {camera_index} with {backend_name} failed to open")
                    continue
                
                print(f"  ✓ Camera {camera_index} opened with {backend_name}")
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret and frame is not None:
                    height, width = frame.shape[:2]
                    print(f"  ✓ Successfully read frame: {width}x{height}")
                    print(f"  ✓ Camera {camera_index} is WORKING!")
                    cap.release()
                    return camera_index, backend
                else:
                    print(f"  ❌ Camera opened but cannot read frames")
                    cap.release()
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                if 'cap' in locals():
                    cap.release()
    
    print("\n" + "=" * 50)
    print("❌ No working camera found!")
    print("\nTroubleshooting tips:")
    print("1. Make sure your camera is connected")
    print("2. Close other applications that might be using the camera")
    print("3. Check Windows Camera privacy settings")
    print("4. Try unplugging and replugging USB cameras")
    print("5. Restart your computer if the camera was recently connected")
    return None, None

if __name__ == "__main__":
    camera_index, backend = test_camera()
    if camera_index is not None:
        print(f"\n✅ Camera test successful!")
        print(f"   Use camera index: {camera_index}")
        sys.exit(0)
    else:
        print(f"\n❌ Camera test failed!")
        sys.exit(1)

