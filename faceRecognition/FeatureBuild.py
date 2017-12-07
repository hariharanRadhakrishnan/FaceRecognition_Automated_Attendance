#Using the 68 landmark points identify the features of the face
def build_dlib_features(points):

    face_curve = points[:17]
    left_eyebro = points[17:22]
    right_eyebro = points[22:27]
    nose = points[27:36]
    left_eye = points[36:42]
    right_eye = points[42:48]
    mouth = points[48:58]

    features = [face_curve,left_eyebro,right_eyebro,nose,left_eye,right_eye,mouth]
    return features

#Using the 68 points build the voronoi face mesh
def build_voronoi_features(points):
	pass