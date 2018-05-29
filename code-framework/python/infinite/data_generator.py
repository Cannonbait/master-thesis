import numpy as np
import worker_pool

def _generate_dimensions(settings):
    dimensions = []
    for key in settings.trial_ranges:
        if len(settings.trial_ranges[key]) > 2:
            dimensions.append((key, np.arange(settings.trial_ranges[key][0], settings.trial_ranges[key][1]+1, settings.trial_ranges[key][2])))
    return dimensions

def _convert_to_list(results, settings):
    result_list = list(range(0, len(results)))

    for result in results:
        result_list[result[0]] = (result[1], result[2])
    return result_list


# Entry point method
def generate_data(settings):
    # Check that each pattern generator is an instance of the interface

    controller = worker_pool.Controller()
    trials = []
    for i, k in enumerate(np.arange(settings.k[0], settings.k[1], settings.k[2])):
        trials.append(k)
    return(controller.test(trials, settings))
    
