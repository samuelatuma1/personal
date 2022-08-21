const nodemailer = require("nodemailer")
const crypto = require("crypto")
const {JWTService} = require("./jwt.service.js")

class Mail{
    /**
     * @desc instantiates mail data
     * @param service : Mail service Provide
     * @param email_username : Sender email address 
     * @param email
     */
    constructor(service, email_username, email_password){
        this.service = service
        this.email_username = email_username,
        this.email_password = email_password

    }
    createTransport = () => {
        return nodemailer.createTransport({
            service: this.service,
            auth: {
                user: this.email_username,
                pass: this.email_password
            }
        })
    }
    sendMail = async (to, subject, html) => {
        try{
            const transporter = this.createTransport()
            const mailRequest = await transporter.sendMail({from: this.email_username, to, subject, html})
            console.log(mailRequest)
            return mailRequest

        } catch(err){
            return {error: "An error occured while sending mail"+ `Mail to ${to} not sent`}
        }
    }

    sendVerificationMail = async (req, savedUser) => {
       
        try{
            const to = savedUser.email
            const fullName = savedUser.fullName || "there"

            const signedToken = JWTService.signToken({email: to}, process.env.JWT_KEY,
                (60 * 60 * 5))
            const verificationUrl = req.protocol + '://' + req.get('host') 
                + "/auth/verifyMail" + "/" + signedToken
        
            const verificationMail = `
                <html>
                    <body style="font-family: verdana sans-serif;">
                        <h3>Hello ${fullName}</h3>
                        <p>Please confirm your email by clicking the button below.</p>

                        <button style="background: teal; color: white; border: 0px solid teal; 
                            border-radius: 5px; padding: 10px;">
                                <a href="${verificationUrl}" style="color: inherit;
                                text-decoration: none;">Verify</a>
                            </button>
                        <p>Didn't sign up for our mail, Please email us at ...</p>
                    </body>
                </html>`    

                const sendMail = await this.sendMail(to, "Verify Email", verificationMail)
                return sendMail
        } catch(err){
            console.log(err)
            throw new Error(err)
        }
    }

}

module.exports = {Mail}