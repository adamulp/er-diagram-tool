import svgwrite


# Function to create an SVG with text
def create_text_svg(
    filename, text, font_weight="normal", font_style="normal", underline=False
):
    dwg = svgwrite.Drawing(filename, profile="tiny", size=("100px", "100px"))

    # Add the text to the SVG
    text_element = dwg.text(
        text,
        insert=("50%", "60%"),  # Adjust the y-position to manually center the text
        font_size="80px",
        font_family="Times New Roman",
        font_weight=font_weight,
        font_style=font_style,
        text_anchor="middle",
    )
    dwg.add(text_element)

    # If underline is needed, add a line element manually
    if underline:
        dwg.add(
            dwg.line(
                start=("25%", "75%"),  # Starting point of the line
                end=("75%", "75%"),  # Ending point of the line
                stroke=svgwrite.rgb(0, 0, 0, "%"),
                stroke_width=5,  # Adjust the thickness of the underline
            )
        )

    dwg.save()


# Create the SVG files
create_text_svg("bold.svg", "B", font_weight="bold")
create_text_svg("italic.svg", "I", font_style="italic")
create_text_svg("underline.svg", "U", underline=True)

print("SVG files created successfully!")
