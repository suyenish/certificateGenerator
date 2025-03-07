from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import io

app = Flask(__name__)

# Register fonts that support multilingual text
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))  # For Kazakh & Russian
pdfmetrics.registerFont(TTFont('NotoSansKR', 'NotoSansKR-Regular.ttf'))  # For Korean
pdfmetrics.registerFont(TTFont('dvs', 'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('dvsb', 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('tnr', 'tnr.ttf'))
pdfmetrics.registerFont(TTFont('tnrb', 'tnrb.ttf'))
pdfmetrics.registerFont(TTFont('tnrbi', 'tnrbi.ttf'))
pdfmetrics.registerFont(TTFont('tnri', 'tnri.ttf'))



def generate_pdf(data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setTitle(f"{data['number_cer']}")
    # Set up fonts
    image = "header.png"
    pdf.drawImage(image, 50, 650, width=495, height=150)

    # Certificate info
    pdf.setFont("tnr", 14)
    pdf.drawString(50, 630, f"№ {data['number_cer']}")
    formatted_doc = datetime.strptime(data['doc'], "%Y-%m-%d").strftime("%d.%m.%Y")
    pdf.drawString(50, 615, f"{formatted_doc}")

    # To whom
    pdf.setFont("tnrbi", 14)
    pdf.drawString(50, 575, "To whom it may concern")

    # Main
    #     f"The Consular section of the Consulate General of the Republic of Kazakhstan in Busan "
    #     f"hereby certifies that according to the Driver’s license number: {data['license_number']}, "
    #     f"citizen of the Republic of Kazakhstan {data['gender']} {data['full_name']} (Date of birth: {data['dob']}), "
    #     f"passport number: {data['passport_number']} is allowed to drive motor vehicles under "
    #     f"the category {data['vehicle_categories']}."
    pdf.setFont("tnr", 14)
    pdf.drawString(50, 520, "The Consular section of the Consulate General of the Republic of Kazakhstan")
    pdf.drawString(50, 500, "in Busan hereby certifies that the following individual holds a valid driver's license")
    pdf.drawString(50, 480, "issued by the Republic of Kazakhstan and is authorized to operate motor vehicles")
    pdf.drawString(50, 460, "under the specified categories.")
    formatted_dob = datetime.strptime(data['dob'], "%Y-%m-%d").strftime("%d.%m.%Y")
    pdf.drawString(50, 430, f"Name: {formatted_dob}")

    pdf.drawString(50, 405, f"Date of Birth:{data['dob']}")
    pdf.drawString(50, 380, f"Passport Number: {data['passport_number']}")
    pdf.drawString(50, 355, f"Permanent address: Kazakhstan")
    pdf.drawString(50, 330, f"Driver’s license registration number: {data['license_number']}")
    pdf.drawString(50, 305, f"Categories of driver’s license: {', '.join(data['vehicle_categories'])}")
    formatted_doi = datetime.strptime(data['doi'], "%Y-%m-%d").strftime("%d.%m.%Y")
    pdf.drawString(50, 280, f"Date of issue of the license: {formatted_doi}")
    formatted_doe = datetime.strptime(data['doe'], "%Y-%m-%d").strftime("%d.%m.%Y")
    pdf.drawString(50, 255, f"Date of expiry of the license: {formatted_doe}")

    # Signed by
    pdf.setFont("tnrb", 14)
    pdf.drawString(50, 210, f"{data['consul']}_________________________")
    pdf.drawString(50, 180, f"Consulate General of Republic of Kazakhstan")
    pdf.setFont("NotoSansKR", 14)
    pdf.drawString(50, 150, "* 운전면허증 진위확인 후 발급하였음.")

    pdf.save()
    buffer.seek(0)
    return buffer


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            "number_cer":request.form['number_cer'],
            "doc":request.form['doc'],
            "full_name": request.form['full_name'],
            "license_number": request.form['license_number'],
            "passport_number": request.form['passport_number'],
            "dob": request.form['dob'],
            "doi": request.form['doi'],
            "doe": request.form['doe'],
            "gender": request.form['gender'],
            "vehicle_categories": request.form.getlist('vehicle_categories'),
            "consul": request.form['consul']
        }

        pdf_buffer = generate_pdf(user_data)
        return send_file(pdf_buffer, as_attachment=True,
                         download_name=f"{user_data['number_cer']}.pdf",
                         mimetype="application/pdf")

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
