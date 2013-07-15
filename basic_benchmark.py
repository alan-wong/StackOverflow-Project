import competition_utilities as cu
import features
from sklearn.ensemble import RandomForestClassifier

train_file = "train-sample.csv"
#train_file = "train-sample_October_9_2012_v2.csv"
full_train_file = "train.csv"
#full_train_file = "train_October_9_2012.csv"
test_file = "public_leaderboard.csv"
submission_file = "basic_benchmark5.csv"

feature_names = [ "BodyLength"
                , "NumTags"
                , "OwnerUndeletedAnswerCountAtPostTime"
                , "ReputationAtPostCreation"
                , "TitleLength"
                , "UserAge"
                ]

open_status = { 'not a real question' : 1
               ,'not constructive' : 2
               , 'off topic' : 3
               , 'open' : 4
               , 'too localized' : 5
               }

def convert_status(status):
    return open_status[status]

def main():
    print("Reading the data")
    data = cu.get_dataframe(train_file)
    data['OpenStatusMod'] = data['OpenStatus'].map(convert_status)
    #print(data['OpenStatusMod'])

    print("Extracting features")
    fea = features.extract_features(feature_names, data)
    #print(fea.columns)

    print("Training the model")
    rf = RandomForestClassifier(n_estimators=50, verbose=2, compute_importances=True, n_jobs=-1, random_state = 0)
    print("Training the model, created RFC")
    #rf.fit(fea, data["OpenStatus"])
    rf.fit(fea, data["OpenStatusMod"])

    print("Reading test file and making predictions")
    #data = cu.get_dataframe(test_file)
    data = cu.get_dataframe(full_train_file)
    print("Reading data frame")
    data['OpenStatusMod'] = data['OpenStatus'].map(convert_status)
    print("adding column")
    test_features = features.extract_features(feature_names, data)
    print("extract features")
    probs = rf.predict_proba(test_features)

#    print("Calculating priors and updating posteriors")
#    new_priors = cu.get_priors(full_train_file)
#    old_priors = cu.get_priors(train_file)
#    print "new priors %s" %(new_priors)
#    print "old priors %s" %(old_priors)
#    probs = cu.cap_and_update_priors(old_priors, probs, new_priors, 0.001)

    print("Saving submission to %s" % submission_file)
    cu.write_submission(submission_file, probs)

if __name__=="__main__":
    main()