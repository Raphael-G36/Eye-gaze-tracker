"""
Simple camera check script - run this to test if your camera works
"""
import cv2
import sys

print("=" * 60)
print("Camera Diagnostic Tool")
print("=" * 60)

# Try simple camera access
print("\n1. Testing basic camera access (index 0)...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("   ✓ Camera index 0 opened successfully")
        
        print("\n2. Testing frame read...")
        ret, frame = cap.read()
        if ret and frame is not None:
            height, width = frame.shape[:2]
            print(f"   ✓ Frame read successful!")
            print(f"   ✓ Frame size: {width}x{height}")
            print("\n✅ Camera is working correctly!")
            cap.release()
            sys.exit(0)
        else:
            print("   ✗ Camera opened but cannot read frames")
            cap.release()
    else:
        print("   ✗ Camera index 0 failed to open")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Try DirectShow on Windows
if sys.platform == 'win32':
    print("\n3. Testing DirectShow backend (Windows)...")
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            print("   ✓ DirectShow camera opened")
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                print(f"   ✓ Frame read successful!")
                print(f"   ✓ Frame size: {width}x{height}")
                print("\n✅ Camera works with DirectShow backend!")
                cap.release()
                sys.exit(0)
            cap.release()
        else:
            print("   ✗ DirectShow failed to open camera")
    except Exception as e:
        print(f"   ✗ DirectShow error: {e}")

# Try other camera indices
print("\n4. Testing other camera indices...")
for idx in [1, 2]:
    try:
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"   ✓ Camera index {idx} works!")
                cap.release()
                sys.exit(0)
            cap.release()
    except:
        pass

print("\n" + "=" * 60)
print("❌ No working camera found!")
print("=" * 60)
print("\nTroubleshooting steps:")
print("1. Make sure your camera is connected")
print("2. Close all other applications using the camera:")
print("   - Zoom, Teams, Skype, Camera app, etc.")
print("3. Check Windows Camera Privacy Settings:")
print("   - Settings → Privacy → Camera")
print("   - Enable 'Allow apps to access your camera'")
print("   - Enable 'Allow desktop apps to access your camera'")
print("4. Try unplugging and replugging USB cameras")
print("5. Restart your computer")
print("=" * 60)

sys.exit(1)

