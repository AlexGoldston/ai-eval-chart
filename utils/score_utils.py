# scoring helper functions

def determine_quadrant(complexity, time):
    if complexity >= 50 and time < 50:
        return "HIGH EFFORT, QUICK WINS"
    elif complexity >= 50 and time >= 50:
        return "STRATEGIC INVESTMENTS"
    elif complexity < 50 and time < 50:
        return "QUICK WINS"
    else:
        return "LONG TERM LOW EFFORT"
    
def calculate_overall_score(cost, speed, culture, quality, long_term, complexity, time):
    impact_score = (
        0.1 * cost +
        0.1 * speed +
        0.1 * culture +
        0.2 * quality +
        0.5 * long_term
    )
    effort_score = (complexity + time) / 2
    effort_modifier = 1 - (effort_score / 200)
    return round(impact_score * (1 + effort_modifier), 2)