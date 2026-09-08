# python main.py

import math
from PIL import Image

# ベクトルの足し算
def vec_add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2]) 

# ベクトルの引き算
def vec_sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

# 内積計算
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

# 外積計算
def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1], 
        a[2]*b[0] - a[0]*b[2], 
        a[0]*b[1] - a[1]*b[0]  
    )

# ベクトルの大きさ（ノルム）を計算
def norm(a):
    result = math.sqrt(dot(a, a))
    return result

# ベクトルの正規化
def normalize(a):
    a_len = norm(a)  
    return (
        a[0] / a_len,  
        a[1] / a_len,  
        a[2] / a_len    
    )

# ベクトルのスカラー倍
def vec_scale(s, a):
    return (s*a[0], s*a[1], s*a[2]) 

# ==================================
# 各種パラメータの設定
# ==================================

# カメラについて
camera_pos   = (3, 2, 5)   # カメラの位置
camera_focus = (1, 1, 1)   # カメラの注視点

# 球について
sphere_pos = (2, 1, 2)     # 球の中心位置
radius     = 1             # 球の半径
(red, green, blue) = (0, 0, 255)

# 光源の位置
light_pos = (4, 3, 2)

# 画像サイズ
width  = 200
height = 200
img = Image.new("RGB", (width, height))

# ==================================
# カメラ座標系の構築
# ==================================

# カメラの前方向ベクトルを計算
camera_forward_vec = vec_sub(camera_focus, camera_pos)  
camera_forward_vec = normalize(camera_forward_vec) 

# 世界の上方向ベクトル
world_up = (0, 1, 0)

# カメラの右方向ベクトル
camera_right_vec = cross(camera_forward_vec, world_up)  
camera_right_vec = normalize(camera_right_vec)  

# カメラの上方向ベクトル
camera_up_vec = cross(camera_right_vec, camera_forward_vec)  
camera_up_vec = normalize(camera_up_vec) 

# 全画素に対して描画ループ
for x in range(width):
    for y in range(height):

        # ピクセルを[-1, 1]に正規化
        px = (x - width/2)  / (width/2) 
        py = (y - height/2) / (height/2) 

        # 視線（レイ）のベクトル
        ray_vec = (
            px * camera_right_vec[0] + py * camera_up_vec[0] + camera_forward_vec[0], 
            px * camera_right_vec[1] + py * camera_up_vec[1] + camera_forward_vec[1], 
            px * camera_right_vec[2] + py * camera_up_vec[2] + camera_forward_vec[2]
        )
        ray_vec = normalize(ray_vec)
        # print(f"ray_vec = {ray_vec[0]}, {ray_vec[1]}, {ray_vec[2]}")

        # 視線ベクトルと球面の方程式の連立方程式
        # |camera_pos_vec + t * ray_vec - sphere_pos_vec|^2 = 1
        oc_vec = vec_sub(camera_pos, sphere_pos)
        a = dot(ray_vec, ray_vec)
        b = 2*dot(oc_vec, ray_vec)
        c = dot(oc_vec, oc_vec) - radius**2
        # print(f"({a})*t^2 + ({b})*t +({c}) = 0")
        discriminant = b*b - 4*a*c

        # 視線と球が衝突（実数解あり）
        if discriminant >= 0:
            t = (-b - math.sqrt(discriminant)) / (2*a)

            # 視線と球の衝突点
            hit_point = (
                camera_pos[0] + t*ray_vec[0], 
                camera_pos[1] + t*ray_vec[1], 
                camera_pos[2] + t*ray_vec[2]
            )

            # 球の単位法線ベクトル
            normal_vec = normalize(vec_sub(hit_point, sphere_pos))

            # 光源ベクトル
            light_vec = normalize(vec_sub(light_pos, hit_point))

            # 拡散反射（明るさの計算）
            direct_intensity = max(0, dot(normal_vec, light_vec))
            
            # 最終的な明るさを計算し色を計算
            intensity = 0.2 + (1 - 0.2)*direct_intensity
            (red_output, green_output, blue_output) = (red*intensity, green*intensity, blue*intensity)

            # 出力
            print(f"({red_output}, {green_output}, {blue_output})")
            img.putpixel((x, y), (int(red_output), int(green_output), int(blue_output)))
        
        # 視線と球が衝突しない（実数解なし）
        else:
            print("50 50 50")
            img.putpixel((x, y), (50, 50, 50))

# 画像をファイルに保存する
img.save("output.png")

