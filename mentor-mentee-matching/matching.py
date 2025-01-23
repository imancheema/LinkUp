# matching.py
import pandas as pd

def match_attributes(mentee_field, mentor_field):
    mentee_set = set(str(mentee_field).split(','))
    mentor_set = set(str(mentor_field).split(','))
    return len(mentee_set & mentor_set)

def calculate_match_score(mentee, mentor):
    identity_match = match_attributes(mentee['Check all of the words that relate to your identity.'], mentor['Check all of the words that relate to your identity'])
    communication_match = match_attributes(mentee['How would you prefer to communicate with your mentor?  '],
                                            mentor['How would you prefer to communicate with your mentee?'])
    discipline_match = match_attributes(mentee['Discipline/Major?'], mentor['Discipline/Major?'])
    support_match = match_attributes(mentee['What support do you need from a mentor to help with your growth?  '],
                                     mentor['What can you offer as a mentor, and how can you support a mentee\'s growth?  '])
    growth_support_match = match_attributes(mentee['What support do you need from a mentor to help with your growth?  '],
                                            mentor['What can you offer as a mentor, and how can you support a mentee\'s growth?  '])

    total_score = identity_match + communication_match + discipline_match + support_match + growth_support_match
    return total_score

def matching_process(mentees_df, mentors_df):
    matched_pairs = []
    matched_mentor_names = set()
    unmatched_mentees = []

    for _, mentee in mentees_df.iterrows():
        best_match = None
        highest_score = 0

        for _, mentor in mentors_df.iterrows():
            if mentor['Full Name'] in matched_mentor_names:
                continue

            total_score = calculate_match_score(mentee, mentor)

            if total_score > highest_score:
                best_match = mentor
                highest_score = total_score

        if best_match is not None:
            matched_pairs.append((mentee['Full Name'], best_match['Full Name']))
            matched_mentor_names.add(best_match['Full Name'])
        else:
            unmatched_mentees.append(mentee['Full Name'])

    remaining_mentors = mentors_df[~mentors_df['Full Name'].isin(matched_mentor_names)]

    # pair each mentee with a mentor in order based on their positions in the list, using zip
    for mentee_name, mentor_name in zip(unmatched_mentees, remaining_mentors['Full Name']):
        matched_pairs.append((mentee_name, mentor_name))

    return matched_pairs
