import numpy as np
import matplotlib.pyplot as plt
from const import Magnification, Camera

class OpticalSystem:
    def __init__(self, magnification):
        self.magnification = magnification
        self.img_array = self.load_image()
        self.real_width, self.real_height = self.calculate_real_dimensions()
        self.real_center = (self.real_width/2 , self.real_height/2)

    def load_image(self):
        array_file_path = self.magnification.value.file_name
        return np.load(array_file_path)

    def calculate_real_dimensions(self):
        width, height = Camera.Sensor_Size
        real_width = width * Camera.Pixel_Size / self.magnification.value.mag
        real_height = height * Camera.Pixel_Size / self.magnification.value.mag
        return real_width, real_height

    def draw_center_square(self, ax, size_um, show_coordinates=True):
        # 마이크로미터를 픽셀로 변환
        size_pixels = size_um * self.magnification.value.mag / Camera.Pixel_Size
        
        # 이미지 중심 계산
        center_x = self.real_width / 2
        center_y = self.real_height / 2
        
        # 정사각형의 좌표 계산
        half_size = size_um / 2
        left = center_x - half_size
        right = center_x + half_size
        top = center_y - half_size
        bottom = center_y + half_size
        
        # 정사각형 그리기
        square = plt.Rectangle((left, top), size_um, size_um, 
                               fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(square)
        
        if show_coordinates:
            # 꼭짓점 좌표 표시
            corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
            for i, (x, y) in enumerate(corners):
                ax.text(x, y, f'({x:.2f}, {y:.2f})', color='red', fontsize=8, 
                        ha='right' if i in [0, 3] else 'left', 
                        va='bottom' if i in [0, 1] else 'top')
        
        # 실제 크기 표시
        ax.text(right + 5, center_y, f'{size_um} µm', color='red', fontsize=10, 
                rotation=270, va='center')
        
    def add_scale_bar(self, ax, length_um, thickness_pixels=2, color='white', position='lower left', font_size=10):
        # 마이크로미터를 픽셀로 변환
        length_pixels = length_um * self.magnification.value.mag / Camera.Pixel_Size
        
        # 스케일바 위치 설정
        margin = 0.05  # 여백 (이미지 크기의 5%)
        if position == 'lower right':
            start_x = self.real_width - length_um - margin * self.real_width
            start_y = self.real_height - margin * self.real_height
        elif position == 'lower left':
            start_x = margin * self.real_width
            start_y = self.real_height - margin * self.real_height
        else:
            raise ValueError("지원되지 않는 위치입니다. 'lower right' 또는 'lower left'를 사용하세요.")

        # 스케일바 그리기
        ax.plot([start_x, start_x + length_um], [start_y, start_y], 
                color=color, linewidth=thickness_pixels)
        
        # 스케일바 텍스트 추가
        ax.text(start_x + length_um / 2, start_y - thickness_pixels,
                f'{length_um} µm', color=color, ha='center', va='top',
                fontsize=font_size, fontweight='bold',
                )
        
        

    def display_image(self, square_size_um=10 ,show_square = False,show_scale_bar =False ,scale_bar_length_um =10):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(self.img_array, extent=[0, self.real_width, self.real_height, 0])
        if show_square:
            self.draw_center_square(ax, square_size_um)
            
        if show_scale_bar:
            self.add_scale_bar(ax, scale_bar_length_um)
            
        plt.show()

# 사용 예시
if __name__ == "__main__":
    optical_system = OpticalSystem(Magnification.X50)
    optical_system.display_image(show_square= True ,show_scale_bar=True)


    

