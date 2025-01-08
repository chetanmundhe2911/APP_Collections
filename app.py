import os
from fpdf import FPDF
from PIL import Image
import streamlit as st

# Function to compress images
def compress_image(image_path, quality=50, max_width=800):
    """
    Compress the image by resizing and reducing its quality.
    :param image_path: Path to the image file.
    :param quality: Quality of the compressed image (1-100).
    :param max_width: Maximum width of the image to resize.
    :return: Bytes object of the compressed image.
    """
    try:
        with Image.open(image_path) as img:
            # Resize image while maintaining aspect ratio
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed
            if img.mode == "RGBA":
                img = img.convert("RGB")

            # Save to in-memory bytes
            compressed_path = image_path.replace(".png", "_compressed.jpg")
            img.save(compressed_path, "JPEG", quality=quality)
            return compressed_path
    except Exception as e:
        print(f"Error compressing image {image_path}: {e}")
        return None

# Function to create a PDF from uploaded images
def create_pdf_from_uploaded_images(uploaded_files):
    """
    Create a PDF from uploaded image files.
    :param uploaded_files: List of Streamlit UploadedFile objects.
    :return: Bytes object of the created PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    temp_files = []

    for uploaded_file in uploaded_files:
        try:
            # Save the uploaded image temporarily
            img_path = os.path.join("temp", uploaded_file.name)
            os.makedirs("temp", exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Compress the image
            compressed_image_path = compress_image(img_path)
            if compressed_image_path:
                temp_files.append(compressed_image_path)

                # Add the compressed image to the PDF
                pdf.add_page()
                pdf.image(compressed_image_path, x=10, y=10, w=180)
        except Exception as e:
            print(f"Error processing {uploaded_file.name}: {e}")
    
    # Save PDF to in-memory bytes
    pdf_path = "output.pdf"
    pdf.output(pdf_path)

    # Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)
    for uploaded_file in uploaded_files:
        temp_path = os.path.join("temp", uploaded_file.name)
        if os.path.exists(temp_path):
            os.remove(temp_path)
    os.rmdir("temp")

    return pdf_path

# Streamlit App
def main():
    # Set up the page config
    st.set_page_config(page_title="Image to PDF Converter", page_icon="🖼️", layout="wide")
    st.markdown(
        """
        <style>
        .main-content {text-align: center;}
        body {background-color: #f5f5f5;}
        .title {color: #3498db;}
        .intro-text {color: #e74c3c;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 class='title'>🖼️ Image to PDF Converter 🎉</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 class='intro-text'>Effortlessly compress images and convert them into a single PDF</h3>",
        unsafe_allow_html=True
    )

    st.sidebar.title("✨ Customize")
    bg_color = st.sidebar.color_picker("Choose Background Color", "#ffffff")
    text_color = st.sidebar.color_picker("Choose Text Color", "#000000")
    st.sidebar.markdown("---")
    st.sidebar.markdown("📥 Upload images to get started!")

    # Upload images
    st.header("🔼 Upload Your Images")
    st.markdown("Upload PNG or JPEG files to create your custom PDF.")
    uploaded_files = st.file_uploader(
        "Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True
    )

    # Check if images are uploaded
    if uploaded_files:
        st.success(f"{len(uploaded_files)} images uploaded successfully!")
        
        # Display image previews
        st.header("👀 Uploaded Image Previews")
        columns = st.columns(3)
        for idx, uploaded_file in enumerate(uploaded_files):
            with columns[idx % 3]:
                st.image(uploaded_file, use_column_width=True, caption=uploaded_file.name)
    
    # Button to generate the PDF
    if st.button("📄 Convert to PDF"):
        if not uploaded_files:
            st.error("Please upload images to convert.")
        else:
            with st.spinner("Processing your PDF... ⏳"):
                try:
                    # Generate the PDF
                    pdf_path = create_pdf_from_uploaded_images(uploaded_files)
                    with open(pdf_path, "rb") as f:
                        st.success("🎉 PDF created successfully!")
                        st.download_button(
                            "📥 Download PDF", f, file_name="output.pdf", mime="application/pdf"
                        )
                    os.remove(pdf_path)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
