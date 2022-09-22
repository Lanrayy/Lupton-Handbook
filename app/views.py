from flask import render_template, request, flash, redirect, url_for, session
from app import app
# import markdown
from flaskext.markdown import Markdown

@app.route('/', methods=['GET', 'POST'])
def index():
    #if user clicks the buttton, get button info and save data in a session
    if request.method == 'POST':
        try:
            # request info of requested page
            menu_requested = request.form['button']
            # flash("Menu requested: " + menu_requested)
            # if menu_requested == "quick_info":
            #     session['page_requested'] = "quick_info"
            #     return redirect(url_for('info'))
            # save info in a session and redirect to info page
            session['menu_requested'] = menu_requested
            # flash("Succcess", 'alert, alert-success')
            return redirect(url_for('submenu'))
        except Exception as e:
            flash("Try again! An error occured")
    return render_template('index.html',
                           title='Lupton Handbook')

#Used to display all the pages in a menu
@app.route('/submenu', methods=['GET', 'POST'])
def submenu():
    if session["menu_requested"] == None:
        flash("Found")
    # get list of buttons
    page_title = get_pages(session["menu_requested"])[2]
    
    values = get_pages(session["menu_requested"])[0] # values of the button
    button_text = get_pages(session["menu_requested"])[1] # Button label
    page_title = get_pages(session["menu_requested"])[2]

    # flash(values)
    # If user clicks the back to homepage button buttton
    if request.method == 'POST':
        try:
            page_requested = request.form['button'] # check which button was clicked
            # flash(page_requested)
            if page_requested == "back":
                return redirect(url_for('index'))
            else:
                session['page_requested'] = page_requested # save page title
                return redirect(url_for('info'))
        except Exception as e:
            flash("Try again! An error occured")
    return render_template('submenu.html',
                            title = "Lupton Handbook",
                            page_title = page_title,
                            values = values,
                            len = len(values),
                            button_text = button_text)

# This function is used on the sub menu page - it returns a list of menu buttons for the sub menu page
# return submenu item of a main menu page
def get_pages(key):
    switcher = {
        #main menu  | sub menu
        "quick_info" : [["rla_info","security","lsmp", "lockouts"],
                        ["RLA Info","Security", "LSMP", "Lockouts"], 
                        "Quick Info"],
        "fire" : [["actual_fire", "fire_alarm", "fire_drill", "fire_equipment_tampered"],  # values
                ["Actual Fire", "Fire Alarm", "Fire Drill", "Fire Equipement Tampered With"],    # Button Text
                "Fire"],                                        # Main menu title
        "maintenance" : [["maintenance", "damages", "vandalism"],
                        ["Maintenance", "Damages", "Vandalism"], 
                        "Maintenance / Damage"],
        "parties": [["parties", "smoking_in_flats", "drugs"],
                    ["Parties", "Smoking in Flats", "Drugs"],
                    "Parties"],
        "medical_assistance" :[["non_immediate_medical_issue","accident_or_illness", "recovery_position", "over_intoxication", "substance_use_concerns"],
                                ["Non-Immediate Medical Issue","Accidents or Illness", "Recovery Position", "Over Intoxication", "Substance Use Concerns"],
                                "Medical Assistance"],
        "student_welfare": [["welfare_check", "missing_student", "mental_health", "suicide_attempt", "harrassment_and_bullying"],
                            ["Welfare Check", "Missing Student", "Mental Health", "Suicide Attempt", "Harrassment and Bullying"],
                            "Student Welfare"],
        "sexual_violence" : [["sexual_violence_questions","sexual_violence_documentation", "historic_disclosure","recent_disclosure"],
                            ["Sexual Violence Questions", "Sexual Violence Documentation", "Historic Disclosure", "Recent Disclosure"],
                            "Sexual Violence"],
        "flat_issues": [["flatmate_conflict", "physical_altercation", "food_theft", "tidyness", "theft"],
                            ["Flatmate Conflict", "Physical Altercation", "Food Theft", "Tidyness", "Theft"],
                            "Flat Issues"],
        "miscellaneous":[["emergencies", "weapon", "intruders", "strangers"],
                        ["Emergencies", "Weapon", "Intruders", "Strangers in the building"],
                        "Miscellanous"]
    }
    
    pages = switcher.get(key, ["Try again! not found"])
    return pages

# Info page
@app.route('/info', methods=['GET', 'POST'])
def info():
    # retrieve info from session
    page_title = get_info(session["page_requested"])[0]
    page_content2 = get_info(session["page_requested"])[1]
    page_content = page_content2

    # If user clicks the back button
    if request.method == 'POST':
        try:
            page_requested = request.form['button'] # check which button was clicked
            if page_requested == "back":
                return redirect(url_for('submenu'))
        except Exception as e:
            flash("Try again! An error occured")

    return render_template('info.html',
                            title = "Lupton Handbook",
                            page_title = page_title,
                            page_content = page_content)

# ON the info page
def get_info(key):
    switcher = {
        # page info
        "rla_info" : ["Quick Info", "<b><a href='https://leeds365.sharepoint.com/:w:/r/sites/TEAM-ResidenceLife-Lupton/Shared%20Documents/Lupton/\
                        RLA%20Rota%20Freshers%20Lupton%20Res.docx?d=w713cd4ef3cc74fb79dba8c7a17445373&csf=1&web=1&e=a8gOVw'> RLA Rota</a> </b>\
                        <br> RLA duty mobile:  07903 610116 <br>\
                        Warden Mobile: 07810 852142 <br><br> \
                        <b> KEYS </b> <br>\
                        3474 - Intruder alarm code (Site office) <br> 8L153/ 948: room master key <br>\
                        550 key: fire key <br> SVS: padlocks around campus (front gate padlock) <br><br> \
                        <b>SITE PHONE:</b> <br> 0000- phone password <br> Then 83860 <br> (BEN’s ACCOUNT) <br> "],
        

        "lockouts" : ["Lockouts", "If you need to deal with a lock out, before you can let a student back into their \
                        flat, you must confirm that they are who they claim to be (e.g., by viewing their University\
                         student card, student number or any other identification they may have or asking them to describe their \
                        room and cross-checking their personal details with the occupancy list in Teams or records held in \
                        the Site Office). <br> <b> Don’t simply take their word for it </b>. <br> <br> \
                        After confirming they are who they say they are, access the site office and \
                        make a spare for and/or key for the student. \
                        Write their name and student number on a post-it note and place on the hook."],


        "security" : ["Security","Security: 0113 343 5494 (non-emergencies) \
                        <br> \n Security: 0113 343 2222 (emergencies only) <br> Security Whatsapp: 07876 866747 \
                        <br> Security email: security@leeds.ac.uk"],


        "lsmp" :["LSMP", "4 Blenheim Court <br> \
                        Blenheim Walk <br>Leeds <br>LS2 9AE <br>0113 295 4488 <br> www.leeds.ac.uk/lsmp/<br> <br>\
                        You may also find it useful to call NHS \
                        Direct on 111 if you need medical advice. (http://www.nhsdirect.nhs.uk/)"],


        "actual_fire" : ["Actual Fire", "When there is an <b> actual fire </b>, the buzzer will go off. \
                        In the event of a real fire, pull the fire alarm. Remain calm and evacuate the building\
                        to your designated evacuation point. <br> <b>You should call the fire brigade immediately, followed\
                        by University Security / Private Security (if applicable) and then your Residence Life Warden\
                        to report to incident </b>. Do not attempt to tackle a fire yourself unless you are sure that it is\
                        manageable. Smoke can overpower you very quickly and it is better to be safe and let the \
                        experts deal with the situation. You are not responsible for going through the block to ensure \
                        that all students have evacuated the building, but you should ensure that those that have evacuated \
                        congregate at the designated evacuation point. <br> Once everything has settled and everyone is safe, \
                        Document the incident on StarRez."],


        "fire_alarm" : ["Fire Alarm", "When the fire alarm goes off, check the buzzer for the block with the right panel. <br> <br> \
                        Go to the panel and identify the room. Assist student with leaving the building. Wait for security to arrive. \
                        <br> <br>Document the incident on Starrez."],


        "fire_drill": ["Fire Drill", "These are carried out once per term and you may be asked to assist with\
                        this. The times they are held vary but are usually when most people will be in.If you are asked to\
                        help and you are available, you will meet the site staff before the drill to discuss the plan for\
                        its management. As soon as the alarm sounds, go outside with your room list and, as the students\
                        come out, make them move away from the blocks (it would be dangerous to stay close to them in a\
                        real situation because of falling debris) and gather where the instruction sheets in their rooms\
                        tell them is the assembly point and that they stand in their households. When they are all out,\
                        take a roll call. Students may be readmitted to the block and the alarm silenced when the roll\
                        call is complete. Watch out for people answering with others’ names!. After the drill in completed \
                        Document the incident on Starrez."],


        "fire_equipment_tampered" : ["Fire Equipment Tampered With", "If you happen to notice that a fire\
                        extinguisher in a flat has been let off or smoke/heat detectors have been covered, you need to\
                        make inquiries into why this has happened and attempt to identify those involved.  It is especially\
                        important to report it to the site office so that extinguishers can be checked and re-filled.\
                        <br> <br> Document the incident on Starrez."],


        "maintenance": ["Maintenance", "For non-urgent repairs, students should be encouraged to report the matter themselves\
                        to the site office either by email or by calling in at the site office during opening times. If you \
                        notice any faults in communal areas whilst you are around the site, submit an incident report on the \
                        accommodation portal and this will notify the site team. In an emergency (e.g., serious water leaks, \
                        smell of gas, broken windows, electrical or boiler problems) outside office hours, you should ring \
                        University Security to ask them to call out an engineer to investigate the matter. Please keep a \
                        check on the matter until you are satisfied that it has been dealt with appropriately (do not simply \
                        report the matter and assume that Security will deal with it). Document the incident on Starrez."],


        "damages" : ["Damages", "If damage is caused and you know who was responsible (sometimes they do admit it or tell you who did), \
                        tell the Site Office, as soon as you can, so that the bill may be issued to the correct person. \
                        Tell your RLW too so that they can maintain a record of repeat offenders.Un-attributable damage \
                        (malicious or otherwise) in a flat is charged to the flat. Charges are added to the students’ \
                        accommodation bills.It is, of course, important that we should try to find out who has committed \
                        an offence, not only so that innocent people are not forced to pay for it, but in order to deter \
                        that individual and others from doing it again. The certainty of detection is more of a deterrent \
                        than the damage bill itself. This, of course, may be difficult if residents have developed a code \
                        of silence which could mean that residents will not tell us who damaged something, even if they  \
                        know; however, if you develop your listening skills it is frequently possible to find out who \
                        the guilty party is. Impress on the flat that the level of damage bills can be very high indeed, \
                        and if the culprit does not pay then everyone else does. If damage is caused by a guest, the \
                        person or persons who invited him or her are responsible. Saying someone from another block \
                        did it cuts no ice, as they should not have been invited in if no one was responsible for them, \
                        and obviously house doors should never be left open. Make sure students realise that we \
                        understand that anyone can damage something by accident, and if they come forward and admit \
                        it, they will be charged only the replacement cost. If they do not admit it and are later \
                        identified, however, matters will be more serious. The University takes a very dim view of anyone\
                        who causes a safety and security risk and does nothing about it; examples would be broken glass \
                        left unattended to, water spilt on stairs where someone might slip, etc."],


        "vandalism" : ["Vandalism", "<b> Not Targeted </b> <br> If you come across vandalism in residence it is important to document\
                        the situation on StarRez and submit a maintenance request so it can be cleaned up as soon as possible. \
                        Please include photos when documenting. <br> <br><b> Targeted </b> <br> If the vandalism is targeted at a person or group, \
                        or is offensive in nature, first call security. Do not remove it immediately as security may need to take \
                        photos but cover it up with something to prevent more people from seeing it. Security will work with \
                        you, and if necessary, refer it to the police. Security will arrange for cleaning ASAP. Document the \
                        situation on StarRez in as much detail as possible."],


        "non_immediate_medical_issue" : ["Non-Immediate Medical Issue", "If a student does not need immediate\
                        medical assistance (small cut, etc.) you can use the first aid kit in your duty bag to offer them\
                        a plaster or bandage. Students should be advised to self-treat in the first instance. If they have\
                        a more serious accident you can speak to the student about calling security or 111. <br><br> You can also provide\
                        options on how the student can get to the hospital or walk in clinic. If a student is heading to the hospital,\
                        not by ambulance, it is recommended that they see if there is a friend who will go with them."],


        "accident_or_illness" : ["Accidents or Illness", "If you have to call a doctor, the following information \
                        should be elicited from the patient if possible:<br>• Name <br>• Date of birth <br>• Doctor with whom registered\
                        <br>• Any existing medical conditions (diabetes, epilepsy, allergies, etc.) <br>• Any medication which has been \
                        taken, either regularly or because of present condition <br>• Present symptoms  <br> You will probably be asked if the \
                        patient seems to have a temperature, is in pain, is vomiting, etc. If you have asked the doctor or an ambulance \
                        to come, please make sure there is someone there to let them into the block without delay.<br> <br> Contact details for the\
                         Leeds Student Medical Practice: <br> 4 Blenheim Court <br> \
                        Blenheim Walk <br>Leeds <br>LS2 9AE <br>0113 295 4488 <br> www.leeds.ac.uk/lsmp/ <br>   You may also find it useful to call NHS \
                        Direct on 111 if you need medical advice. (http://www.nhsdirect.nhs.uk/). <br> <br>\
                        The doctors at LSMP there are experienced in dealing with students and there are specialists in areas like sports injuries, travel medicine, etc. Also, the \
                        LSMP is close to campus and some students don’t realise that the LSMP may treat only those registered with it \
                        and not to neglect this until they are actually ill, because this can cause problems. \
                        Of course, in an emergency any GP will see someone not registered locally, but it is much better if they have \
                        access to the medical records. Students should be reassured that they may still consult their family doctor when \
                        they go home for the vacations. <br> <br>  Document the incident on Starrez."],


        "over_intoxication": ["Over Intoxication", "Students are accountable for their own decisions regarding alcohol use. They are also\
                        responsible for knowing, understanding, informing themselves of, and complying with applicable policies and laws\
                        related to alcohol. Alcohol will not be accepted as an excuse or rationale for any misconduct.If you come across \
                        a student who is over intoxicated and needs help, the following steps should be taken:\
                         <br><b> Attending to an intoxicated student </b> <br> • Remain calm <br> • Assess the students' vitals and collect as much information from them as possible\
                        <br>• Ensure the student if in the recover position if necessary. Do not move the student unless it is safe to do so for yourself and the student\
                        <br>• Consult with appropriate professionals to assess the situation (Security, RLW, NHS 111, 999)\
                        <br>• Do not leave the student alone if the situation is deemed unsafe to do so\
                        <br>• Once the student is safe – has gone to bed, is being taken care of by roommates or had been transported \
                        <br>to the hospital, <br><br><b> Document the situation on StarRez </b> <br>.  <br> <b>Information Gathering</b> <br>• How much has the student had to drink?\
                        <br>• What else might the student have in their system?\
                        <br>• What type of activity have they been participating in that evening/day?\
                        <br>• Have their friends given them water or anything to eat recently? <br>• How long have they been vomiting? \
                        <br>• How long have they been in this state? \
                        <br>• What needs to be done to ensure the safety of this student until they sober up (hospital/friends staying with them, etc.)?\
                        <br>• Is anyone else at risk?</b>"],

        "recovery_position" : ["Recovery Position", "<img width:'100px' height='200px' src='{{url_for('static', filename='static/images/recovery-position')}}' alt='Main-image' />"],


        "substance_use_concerns":["Substance Use Concerns", "If a student is experiencing misusing substances (i.e., study drugs, drinking \
                        or using cannabis to cope, etc.), take steps to address the concern with the student. This information may come to \
                        you while the student is currently under the influence, or in conversation with the student or another student after \
                        the fact. Document the situation and/or all the details you have and advise the student of possible next steps. If it \
                        reaches a point in which you are no longer comfortable, or if you need support, call your Residence Life Warden or Security.\
                        Wait with student while Warden arrives. Document the situations. It is important to know that all incidents involving illegal\
                        drugs are followed up with by Security."],


        "missing_student" : ["Missing Student", "If a student is suspected to be missing and there is cause for concern, you should call up to \
                        your Residence Life Warden and explain the situation. Your warden may request that you attend the students flat and \
                        room to check and see if they are present. Once this has been done you should document the situation on StarRez."],


        "welfare_check" : ["Welfare Check", "If someone calls concerned about the safety and wellbeing of a student, a welfare check should be done. \
                        If there are profoundly serious concerns about the student's safety, call security who will attend the call with you.\
                        If security is not needed you should follow the room entry procedures if you need to key in to check on a student. <br> <br> \
                        It is important to note that you cannot call someone back to give them an update on the student. What you can do is try to \
                        contact the student and ask them to call their friend, parents, or whoever requested the welfare check on them, to let \
                        them know they are safe and doing well. If the student is in crisis, follow the proper procedures to provide them with \
                        appropriate support."],


        "mental_health" : ["Mental Health", "You may notice that a student is behaving strangely or is becoming withdrawn; sometimes his or her \
                        friends may draw your attention to this and say that they are worried. <br> <br>If you are concerned about the mental health of \
                        any resident, talk to your RLW immediately. <br><br> <b>  Document the incident on Starrez. </b>"],
        "suicide_attempt" : ["Suicide Attempt", "If a student has attempted suicide, and needs medical attention, call security and explain what \
                        has happened. If possible, provide the room, building, and all information you know. Once Security has been called, call \
                        your Residence Life Warden, who will attend. Document the situation. <br> <br> \
                        These types of situations can be very difficult to deal with – if you need support after responding to a suicide \
                        attempt or helping someone who has suicidal ideations."],


        "harrassment_and_bullying" : ["Harrassment and Bullying", "Both the University and Leeds University Union have strong policies about \
                        all kinds of harassment and bullying. If there is any evidence of any residents being involved in this, it will \
                        count as a major offence and he or she will be referred to a Residential Services disciplinary committee. \
                        Everyone should be treated with respect (difficult though this may be under pressure) and if any student \
                        doesn’t, let your RLW know. For details of the University policy on harassment/bullying, see the Policy \
                        on Dignity and Mutual Respect on the University website."],


        "historic_disclosure" : ["Historic Disclosure ", "1.Respond sensitively to the disclosure by listening, telling \
                        the survivor they believe them, letting the survivor know it was not their fault and avoiding questions \
                        or statements that imply blame, and informing student of ALL limitations to confidentiality. <br> 2. Ask the \
                        student if they are concerned for their safety and wellbeing. If they have expressed thoughts of self-harm or \
                        suicide, follow the Mental Health Crisis procedures <br> 3. Ask the student if they want/require immediate assistance,\
                        support or action. If yes, the Residence Life Warden should be called to attend. a. The Residence Life Warden will \
                        speak with the student, provide options and resources to the students. <br> <b> 4. If the student does not need additional \
                        support the RLW on-call should be called and notified after you finish your conversation with the student. </b><br> 5. You, \
                        or the RLW (if present) should refer the student to the Harassment and Misconduct team who can act as a navigator for \
                        all levels of support and referrals on and off campus. <br>6. When appropriate you can offer to facilitate a warm transfer \
                        by – showing the student the reporting website or walking them to the Misconduct and Harassment office to talk with \
                        an advisor. <br>7. Ask the student if they would like to have their information sent to the Misconduct and Harassment \
                        Team – if yes – this team will reach out and get in touch with the student to provide support. <br> <b> 8. Document in \
                        StarRez with the pre-determined disclosure report that notes the date of the disclosure, the name of the RLA </b>, \
                        identifies that a disclosure of historical, was made and whether: <br> a. Support was identified for the student and \
                        no further action was requested to be taken; or <br> b. The RLW on call was contacted. <br> 9. The Residence Life Warden \
                        or Residence Life Manager may reach out to you and remind you about the resources you can access for support \
                        and feedback. <br> 10. If requested by a student, the Residence Life Officer or Residence Life Manager will \
                        follow-up with information relating to resources and supports on and off campus."],


        "recent_disclosure" : ["Recent Disclosure", "1.Respond sensitively to the disclosure by: listening, telling the survivor \
                        they believe them, letting the survivor know it was not their fault and avoiding questions or statements \
                        that imply blame, and informing student of ALL limitations to confidentiality. <br>2. RLA should inform the \
                        student of their responsibility to call the RLW to attend. <br>3. Ask the student if they are concerned for \
                        their safety and wellbeing. If they have expressed thoughts of self-harm or suicide follow the Mental \
                        Health Crisis procedures. <br>4. Ask the student if they currently feel safe staying in their residence room. \
                        If the student does not feel safe – the warden should be called and will attend to discuss options \
                        with the resident. <br>5. Ask the student if they want/require immediate assistance, support or action. \
                        If yes, you should inform the student of your responsibility to call the Residence Life Warden to \
                        attend, and should call them. <br>a. The Residence Life Warden will speak with the student, provide options \
                        and resources to the students. <br>b. If the student would like to report the incident right away, Security \
                        can be called. Alternatively, you and the student can wait for the Warden to arrive before the student \
                        decides if they would like to call security. <br>6. When calling the warden include as much information as \
                        possible in the call to ensure that there is an accurate transfer of information from RLA to RLW either\
                        over the phone or in- person before the Warden speaks to the student directly – this ensures the student\
                        doesn’t need to tell their story twice if they don’t want to. )<br> 7. The following questions should be \
                        asked to help determine how best to support the survivor <br>8. Whether or not a Warden attends, it is\
                        mandatory to make sure the survivor is aware of the <b> Misconduct & Harassment team </b> . Supply referral \
                        information to the student and let them know they will receive an email from the Residence Life \
                        Team outing supports available on campus<br> 9. Ask the student if they would like to have their \
                        information sent to the Misconduct and Harassment Team – if yes – this team will reach out \
                        and get in touch with the student to provide support <br>10. If the student does not require immediate\
                        assistance, and you believe they are safe, you can provide information on additional supports, and \
                        inform them that you will be calling the warden to let them know about your conversation. The \
                        student will receive an email outlining on and off campus supports – and there will be no additional \
                        follow up unless the student requests it <br> <b> 11. Document in StarRez with the pre-determined disclosure \
                        report that notes the date of the disclosure, the name of the RLA </b>, identifies that a disclosure \
                        was made and whether:a. Support was identified for the student and no further action was \
                        requested to be taken; or b. The RLW on call was contacted <br>12. The Residence Life Warden or \
                        Residence Life Manager may reach out to you and remind youabout the resources you can access for \
                        support and feedback.<br>13. If requested by a student, the Residence Life Officer or Residence \
                        Life Manager will follow-up with information relating to resources and supports on and off campus."],


        "sexual_violence_documentation" : ["Sexual Violence Documentaion", "1.File Incident Report <br> 2. Include Date and Time \
                        <br> 3. Include Location of disclosure <br> 4. Identify (tag) all students involved <br> a. For follow-up, \
                        it will be important that each individual is identified as the ‘survivor’, the ‘respondent’, or a support. \
                        <br>5. Provide the following description: Student “A” disclosed to me an incident of gendered violence involving \
                        student “B”. <br> 6. If this is a historical disclosure and the student does not want to take any action, note \
                        that supports were identified for the student and no further action was requested. <br>7. If this is any other \
                        kind of disclosure, note whether the RLW was required for further immediate assistance. These scenarios \
                        are always to be documented."],


        "sexual_violence_questions" : ["Sexual Violence Questions", "<b>Questions to ask to determine support </b> <br>1. Are you currently feeling safe in your Residence?\
                        <br>2.Do you currently have any concerns about the other individual as it relates to your safety in\
                        Residence? <br> 3. Do you currently have any concerns about the other individual as it relates to your \
                        safety oncampus? <br> 4. Did the assault occur within the last 7 days?<br>5. Do you need medical attention? \
                        <br>6. Do you have any concerns about your physical safety or wellbeing? \
                        <br>7. Would you like to speak to someone who can offer you further support on campus? \
                        <br>8. Would you like to speak with someone about reporting this incident? \
                        <br>9. Do you have any concerns about how this may be impacting your academics? \
                        <br><br>Inform student that the Residence Life may be reaching out to provide information \
                        on supports to the student. Additionally, the reporting party needs to be advised at the time \
                        of the disclosure that their name (and the name of the respondent, if provided) will not be shared \
                        with the Harassment and Misconduct Advisors unless they would like it to be."],


        "parties": ["Parties", "Usually, a named student will be the ‘responsible person’ for the party, and they will be held\
                        responsible for the actions of all guests and any damages caused.  identify the flat residents and/or\
                        the party organiser and tell them (politely) that the party needs to be stopped. <br> If they ignore your\
                        warning or resume the party after you’ve spoken to them, ask them again and warn of consequences (i.e.,\
                        having to call Security for back-up) if it does not stop. Call Security if back-up is needed and let the\
                        Warden(s) know. <br> <br> Document the incident on Starrez."],


        "smoking_in_flats" : ["Smoking in flats", "In accordance with UK legislation, smoking is banned in all open-access communal\
                        areas of the Residences. Kitchens and other public areas are definitely non-smoking. Smoking is not\
                        permitted in any flat, in any residence. If you come across anyone smoking in their rooms or communal \
                        areas of their flats, you should politely ask them to stop or to do so outside of the block dependant \
                        on the time (see Smoke free campus). This includes smoking shishas. You should document the situation \
                        on StarRez so it is recorded, and your Warden can follow up with the student to ensure the situation \
                        is being dealt with appropriately.E-cigarettes are treated the same as smoking regular cigarettes \
                        and students are not permitted to use them inside any of our buildings."],


        "drugs": ["Drugs", "Students should be made aware that the use and possession of cannabis is\
                        still illegal, even buying for flat members if considered supplying and offenders may be prosecuted or \
                        cautioned, at the discretion of the Police. <br><br> A caution, by the way, is never spent, and remains on \
                        one’s record, so, if one is offered a caution as an alternative to prosecution, and accepts it, one is\
                        accepting that it will remain on police files and will be disclosed on Disclosure and Barring checks."],


        "flatmate_conflict" : ["Flatmate conflicts", "If a resident comes to you with concerns about a flatmate, use the active \
                        listening and mediation skills learned in training. Start by listening to the students concerns and encouraging \
                        them to resolve the conflict internally. You can provide tips to you student(s) on how to have a conversation with \
                        their flatmates about the issues they are experiencing. <br><br> After speaking with the student, Document the incident on Starrez. \
                        If the problem is not resolved, offer to facilitate a mediated conversation. If the issue continues, refer the situation to \
                        your warden for further review and continue documenting the situation."],


        "physical_altercation": ["Physical Altercation", "If you come upon a situation where someone has become physically violent or there is a \
                        physical altercation you should call security immediately. DO not touch anyone involved or put yourself in harm's way.\
                        <br> You should not put yourself between two people and should only attempt to stop violent behaviour through verbal intervention \
                        if you feel comfortable. While you are waiting for security to arrive you can focus on clearing the area of others. \
                        <br><br>Document the incident on StarRez."],


        "food_theft": ["Food Theft", "Food going missing or being taken is a complaint that we often receive from students, in some instances \
                        they will name individuals who they believe to be taking it, but very rarely do they have proof. Therefore, dealing with \
                        food thefts can be complicated and often be interwoven with flat politics and relationships. You should understand firstly \
                        that there are many reasons why students take food that is not theirs and it is not always malicious or because of they are lazy. \
                        One reason is financial hardship. Coming to university and living away from home is expensive and factors may mean that some \
                        students find themselves in a position where they cannot afford to buy their own food. If this is the case, we still need to \
                        solve the issue of food going missing (and the financial loss this causes for the owner), but we would do this by supporting \
                        that student in accessing hardship funding which will in time solve the food theft issue. Living communally and sharing \
                        fridges/freezers can also lead to confusion and students taking someone else’s food by mistake; particularly if both \
                        students have brought similar items. You can suggest to all students in the flat that they label their food or create\
                        clearly defined areas in the fridges and freezers so that it is easy for people to see who it belongs too. Lastly, you \
                        want to make sure that there is not an agreement between the flat mates on sharing food or sharing other items, either a\
                        written or unspoken rule. Students can sometimes incorrectly infer that because everyone is happy sharing cutlery or\
                        saucepans that this extends to food, or because one time they were happy to share their milk that this is a standing\
                        agreement. This can be resolved by the flat mates talking to one another and between them setting clear agreements on this. \
                        When dealing with food theft, your role as an RLA is not to blame or accuse anyone, especially if you only have it on hearsay.\
                        Even if everyone in the whole flat is saying it is the same person, it could be a case of the flat ganging up on this one student.\
                        Like most other flat dispute’s communication is key in resolving this, whilst acknowledging that the student who has had their\
                        food taken may be upset and that financial loss for them may have occurred. You should suggest that the students sit down,\
                        when they are calm, as a flat to discuss the food going missing. If they would like support in doing so you could sit in\
                        as a mediator, or they can speak to their RLW. In some instances, if the student who is taking the food realises others\
                        have noticed this can cause them to stop doing so. If the food theft continues, then the RLW can become more involved and\
                        follow up with all individuals in the flat"],


        "theft":["Theft", "If a student comes to you about a theft, you should direct them to file a report with Security. You should then write an\
                        incident report, so your Warden is aware of this situation in case other actions need to be taken. <br><br>Document Incident on StarRez."],
        "tidyness": ["Tidiness and Cleanliness", " Students are responsible for cleaning their own rooms and the communal areas within a flat.\
                        Communal areas are the responsibility of all students. Please make sure that residents keep common areas clean and tidy \
                        for the sake of fellow students. Litter can be a safety hazard – people may slip on flyers left on the stairs, for \
                        instance. Extra cleaning charges may be imposed if there is excessive untidiness, or, in the worst cases, contract \
                        cleaners brought in and the charge passed on to the students. It is always easier to be tough at the beginning and \
                        then ease up – the other way round is almost impossible! Please impress on the residents that they must never throw \
                        things out of their windows. Apart from the fact that this causes unsightly litter, which others have to clear up, \
                        some objects (bottles, etc.) can be dangerous if they hit someone, and throwing food out of the windows attracts rats.\
                        One of the most common problems within a flat is cleanliness of shared kitchens and/or bathrooms so you could suggest \
                        to the students that they have a cleaning rota."],


        "weapon" : ["Weapon", "If you see or a suspect, there may be a weapon in residence you should immediately call security and notify\
                        your warden. <br> Document the incident on StarRez."],


        "intruders" : ["Intruders", "Please keep your eyes open for possible intruders; we have had occasional problems with car vandalism \
                        and break-ins to blocks, and it is vital that everyone should be vigilant. University Security teams regularly \
                        patrol the sites. However, in case of need, telephone University Security. Do (politely) challenge anyone who\
                        appears not to have legitimate business on the site and explain to them that the resident is a private site, \
                        and access is only for those living and working here and their visitors. Unpleasant as it may be, it is \
                        important that visitors should be asked whom they want to see and should not be left alone until that person \
                        has been located however, it is important that you do not put yourself at risk so only challenge someone if \
                        you feel it is safe to do so. <br> <br> Vigilance is particularly important during the vacations (if you’re around) \
                        when the place feels deserted and break-ins are more likely to occur, and at the beginning of the session, \
                        when opportunistic thieves will take advantage of the fact that no one knows anyone else, and students may \
                        leave doors propped open and cars unlocked while transporting belongings."],


        "strangers" : ["Stranger in the building", "If you notice a stranger in the building who doesn’t live there and does not work\
                        for the university, if possible, ask the person to leave the building. If they run away, do not chase them.\
                        Call security and notify them that you’ve seen a stranger in the building. Be mindful of the direction the\
                        person may have travelled to help track them down. If you notice a public disturbance happening outside your\
                        building and the people involved are not students, contact security."],
    }

    info = switcher.get(key, "Try again! not found")
    return info
