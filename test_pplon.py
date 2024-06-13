from pypylon import pylon
import cv2

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

exposure_time = 3000.0
camera.ExposureTime.SetValue(exposure_time)
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# 設置影像保存的檔案名編號
image_counter = 0

# 使用 OpenCV 顯示影像
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(3000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # 訪問影像數據
        image = grabResult.Array
        window = cv2.resize(image, (1440,900))
        cv2.imshow('Camera', window)
        # 按下 's' 鍵拍攝影像並保存
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            image_filename = f"captured_image_{image_counter}.png"
            cv2.imwrite(image_filename, image)
            print(f"Image saved as {image_filename}")
            image_counter += 1

        # 按下 'q' 鍵退出
        if key & 0xFF == ord('q'):
            break

    grabResult.Release()

# 釋放資源
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
