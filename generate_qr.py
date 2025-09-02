#!/usr/bin/env python3
"""
QR Code Generator for Movie Theatre Food Booking System

This script generates QR codes that customers can scan to access the food booking system.
Each QR code contains the URL to the food booking website.

Requirements:
- qrcode[pil] package: pip install qrcode[pil]

Usage:
    python generate_qr.py
"""

import qrcode
import os
from datetime import datetime

def generate_qr_code(url, filename, size=10):
    """
    Generate a QR code for the given URL
    
    Args:
        url (str): The URL to encode in the QR code
        filename (str): The filename to save the QR code as
        size (int): The size of the QR code (default: 10)
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image from QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    img.save(filename)
    print(f"Generated QR code: {filename}")

def main():
    """Main function to generate QR codes"""
    
    # Create qr_codes directory if it doesn't exist
    if not os.path.exists('qr_codes'):
        os.makedirs('qr_codes')
    
    # Base URL for the food booking system
    # Change this to your actual domain when deployed
    base_url = "http://127.0.0.1:8000/"
    
    # Generate main QR code for general access
    main_filename = f"qr_codes/moviesnacks_main_{datetime.now().strftime('%Y%m%d')}.png"
    generate_qr_code(base_url, main_filename, size=15)
    
    # Generate QR codes for different sections (optional)
    sections = [
        ("front_row", "Front Row"),
        ("middle_section", "Middle Section"),
        ("back_section", "Back Section"),
        ("vip_section", "VIP Section")
    ]
    
    for section_id, section_name in sections:
        section_filename = f"qr_codes/moviesnacks_{section_id}_{datetime.now().strftime('%Y%m%d')}.png"
        generate_qr_code(base_url, section_filename, size=12)
    
    print(f"\nGenerated {len(sections) + 1} QR codes in the 'qr_codes' directory")
    print("You can now print these QR codes and place them at the respective seats/sections")
    print(f"Main QR code: {main_filename}")
    
    # Instructions for theatre staff
    print("\n" + "="*60)
    print("INSTRUCTIONS FOR THEATRE STAFF:")
    print("="*60)
    print("1. Print the generated QR codes")
    print("2. Place the main QR code at the entrance and common areas")
    print("3. Place section-specific QR codes at the respective sections")
    print("4. Each seat can use any QR code - they all lead to the same menu")
    print("5. Customers scan the QR code to access the food ordering system")
    print("6. No need to create individual QR codes for each seat")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Error: qrcode package not found!")
        print("Please install it using: pip install qrcode[pil]")
        print("Or install the requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error generating QR codes: {e}")
        print("Please check your setup and try again")
