# # importing the qrcode module  
# import qrcode  
# # creating a QRCode object  
# obj_qr = qrcode.QRCode(  
#     version = 1,  
#     error_correction = qrcode.constants.ERROR_CORRECT_L,  
#     box_size = 10,  
#     border = 4,  
# )  
# # using the add_data() function  
# obj_qr.add_data("https://www.javatpoint.com/python-tutorial")  
# # using the make() function  
# obj_qr.make(fit = True)  
# # using the make_image() function  
# qr_img = obj_qr.make_image(fill_color = "cyan", back_color = "black")  
# # saving the QR code image  
# qr_img.save("qr-img1.png") 

import qrcode

img = qrcode.make("https://www.youtube.com/watch?v=c2gSzYLJ8sY")
img.save("youtube.png")