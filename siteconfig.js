// Site configuration
export const site = {

  // Preset avatars (Gen-Z Indian Avatars powered by Gnani Timbre voices)
  avatars: {
    'Riya': {
      url: './avatars/brunette.glb',
      body: 'F',
      avatarMood: 'neutral',
      fi: 'Riya'
    },

    'Kalpana': {
      url: './avatars/mpfb.glb',
      body: 'F',
      avatarMood: 'happy',
      baseline: {},
      modelDynamicBones: [
        {
          "bone":"LeftBreast",
          "type":"point",
          "stiffness":600,
          "damping":20,
          "deltaLocal":[0,0.01,0],
          "deltaWorld":[0,-0.02,0],
          "limits":[[-0.02,0.02],[-0.02,0.06],[-0.02,0.02],[-0.5,0.5]]
        },
        {
          "bone":"RightBreast",
          "type":"point",
          "stiffness":600,
          "damping":20,
          "deltaLocal":[0,0.01,0],
          "deltaWorld":[0,-0.02,0],
          "limits":[[-0.02,0.02],[-0.02,0.06],[-0.02,0.02],[-0.5,0.5]]
        },
        {
          "bone":"Ponytail1",
          "type":"mix2",
          "stiffness":100,
          "damping":4,
          "limits":[null,null,[null,0.02],null],
          "pivot":true
        },
        {
          "bone":"Ponytail2",
          "type":"mix2",
          "stiffness":150,
          "damping":4,
          "limits":[null,null,[null,0.01],null]
        },
        {
          "bone":"Ponytail3",
          "type":"mix2",
          "stiffness":200,
          "damping":4,
          "limits":[null,null,[null,0.01],null]
        }
      ],
      baseline: {
        headRotateX: -0.01,
        eyeBlinkLeft: 0.05,
        eyeBlinkRight: 0.05
      }
    },

    'Shubham': {
      url: './avatars/avaturn.glb',
      body: 'F',
      avatarMood: 'happy',
      retarget: {
        Hips: { y: 0.03 }, Spine: { y: 0.02 }, Spine1: { y: 0.02, z: 0.01 },
        Spine2: { y: 0.02, z: 0.01 }, Neck: { z: 0.02, y: 0.01 }, Head: { z: 0.02 },
        LeftShoulder: { rx: -0.5 }, RightShoulder: { rx: -0.5 },
        scaleToHipsLevel: 1.0
      },
      baseline: {
        headRotateX: -0.05,
        eyeBlinkLeft: 0.15,
        eyeBlinkRight: 0.15
      }
    },

    'Kabir': {
      url: './avatars/avatarsdk.glb',
      body: 'M',
      avatarMood: 'neutral',
      retarget: {
        Neck: { z: -0.01, rx: -0.15 }, Neck1: { z: -0.01, rx: -0.15 }, Neck2: { z: -0.01, rx: -0.15 },
        LeftShoulder: { rz: -0.3 }, RightShoulder: { rz: 0.3 },
        scaleToEyesLevel: 1.0, origin: { y: -0.1 }
      },
      baseline: {
        headRotateX: -0.04,
        eyeBlinkLeft: 0.05,
        eyeBlinkRight: 0.05
      }
    },

    'Chetana': {
      url: './avatars/vroid.glb',
      body: 'F',
      avatarMood: 'neutral',
      baseline: {
        headRotateX: -0.1,
        eyeBlinkLeft: 0.05,
        eyeBlinkRight: 0.05
      },
      modelDynamicBones: [
        {
          "bone":"J_Sec_L_Bust1",
          "type":"point",
          "stiffness":400,
          "damping":10,
          "deltaLocal":[0,0.01,0],
          "deltaWorld":[0,-0.02,0],
          "limits":[[-0.01,0.01],[-0.01,0.01],[-0.01,0.01],[-0.01,0.01]]
        },
        {
          "bone":"J_Sec_R_Bust1",
          "type":"point",
          "stiffness":400,
          "damping":10,
          "deltaLocal":[0,0.01,0],
          "deltaWorld":[0,-0.02,0],
          "limits":[[-0.01,0.01],[-0.01,0.01],[-0.01,0.01],[-0.01,0.01]]
        },
        {"bone":"J_Sec_Hair2_01","type":"mix2","stiffness":100,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair3_01","type":"mix2","stiffness":150,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair2_02","type":"mix2","stiffness":100,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair3_02","type":"mix2","stiffness":150,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair2_03","type":"mix2","stiffness":100,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair3_03","type":"mix2","stiffness":150,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair2_04","type":"mix2","stiffness":100,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair3_04","type":"mix2","stiffness":150,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair2_05","type":"mix2","stiffness":100,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair3_05","type":"mix2","stiffness":150,"damping":4,"limits":[null,null,[null,0.01],null]},
        {"bone":"J_Sec_Hair2_06","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_06","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair3_06_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_07","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_07","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair3_07_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_08","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_08","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair4_08","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair4_08_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_09","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_09","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair4_09","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair4_09_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_10","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_10","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair3_10_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_11","type":"mix2","stiffness":100,"damping":4},
        {"bone":"J_Sec_Hair3_11","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair3_11_end","type":"mix2","stiffness":200,"damping":4},
        {"bone":"J_Sec_Hair2_12","type":"mix2","stiffness":100,"damping":4,"pivot":true},
        {"bone":"J_Sec_Hair3_12","type":"mix2","stiffness":150,"damping":4},
        {"bone":"J_Sec_Hair2_13","type":"mix2","stiffness":100,"damping":4,"pivot":true},
        {"bone":"J_Sec_Hair3_13","type":"mix2","stiffness":150,"damping":4,},
      ]
    }

  },

  // Official Gnani.ai Timbre v3.0 Indic Voices (Mapped to 3D Avatar Rigs)
  gnaniVoices: {
    "Riya": { id: "Riyaa", model: "timbre-v3.0", avatar: "Riya", lang: "hi-IN", label: "👩 Riya • Riyaa (v3.0)" },
    "Chetana": { id: "Chetana", model: "timbre-v3.0", avatar: "Chetana", lang: "hi-IN", label: "👧 Chetana • Chetana (v3.0)" },
    "Kabir": { id: "Avinash", model: "timbre-v3.0", avatar: "Kabir", lang: "hi-IN", label: "👨 Kabir • Avinash (v3.0)" },
    "Shubham": { id: "Shubham", model: "timbre-v3.0", avatar: "Shubham", lang: "hi-IN", label: "🧑 Shubham • Shubham (v3.0)" },
    "Kalpana": { id: "Kalpana", model: "timbre-v3.0", avatar: "Kalpana", lang: "hi-IN", label: "👱‍♀️ Kalpana • Kalpana (v3.0)" },
    "Kannada": { id: "Avinash", model: "timbre-v3.0", avatar: "Kabir", lang: "kn-IN", label: "🇮🇳 Kannada • Avinash" },
    "Tamil": { id: "Riyaa", model: "timbre-v3.0", avatar: "Riya", lang: "ta-IN", label: "🇮🇳 Tamil • Riyaa" },
    "Telugu": { id: "Chetana", model: "timbre-v3.0", avatar: "Chetana", lang: "te-IN", label: "🇮🇳 Telugu • Chetana" },
  },

  // Gnani Timbre Indic Voices
  googleVoices: {
    "Riyaa (Hindi)": { id: "Riyaa", lang: "hi-IN" },
    "Avinash (Hindi)": { id: "Avinash", lang: "hi-IN" },
    "Shubham (Hindi)": { id: "Shubham", lang: "hi-IN" },
    "Chetana (Hindi)": { id: "Chetana", lang: "hi-IN" },
    "Kalpana (Hindi)": { id: "Kalpana", lang: "hi-IN" },
    "Riyaa (Tamil)": { id: "Riyaa", lang: "ta-IN" },
    "Avinash (Kannada)": { id: "Avinash", lang: "kn-IN" },
    "Chetana (Telugu)": { id: "Chetana", lang: "te-IN" },
  },

  // Gnani Timbre Expressive Voices
  elevenVoices: {
    "Riyaa": { id: "Riyaa" },
    "Avinash": { id: "Avinash" },
    "Shubham": { id: "Shubham" },
    "Chetana": { id: "Chetana" },
    "Kalpana": { id: "Kalpana" },
  },

  // Gnani Timbre Multilingual Indic
  microsoftVoices: {
    "Riyaa (hi-IN)": { lang: "hi-IN", id: "Riyaa" },
    "Avinash (hi-IN)": { lang: "hi-IN", id: "Avinash" },
    "Chetana (hi-IN)": { lang: "hi-IN", id: "Chetana" },
    "Shubham (hi-IN)": { lang: "hi-IN", id: "Shubham" },
    "Kalpana (hi-IN)": { lang: "hi-IN", id: "Kalpana" },
  },

  // Preset views
  views: {
    'DrStrange': { url: './views/strange.jpg', type: 'image/jpg', fi: 'TohtoriOuto' },
    'Matrix': { url: './views/matrix.mp4', type: 'video/mp4' }
  },

  // Preset poses (includes internal poses)
  poses: {
    'Straight': { url: "straight", fi: 'Suora' },
    'Side': { url: "side", fi: 'Keno' },
    'Hip': { url: "hip", fi: 'Lantio' },
    'Turn': { url: "turn", fi: 'Sivu' },
    'Back': { url: "back", fi: 'Taka' },
    'Wide': { url: "wide", fi: 'Haara' },
    'OneKnee': { url: "oneknee", fi: 'Polvi' },
    'TwoKnees': { url: "kneel", fi: 'Polvet' },
    'Bend': { url: "bend", fi: 'Perä' },
    'Sitting': { url:"sitting", fi: 'Istuva' },
    'Dance': { url: './poses/dance.fbx', fi: 'Tanssi' }
  },

  // Preset gestures
  gestures: {
    'HandUp': { name: "handup", fi: 'KäsiYlös' },
    'OK': { name: "ok" },
    'Index': { name: "index", fi: 'Etusormi' },
    'ThumbUp': { name: "thumbup", fi: 'PeukaloYlös' },
    'ThumbDown': { name: "thumbdown", fi: 'PeukaloAlas' },
    'Side': { name: "side", fi: 'Sivu' },
    'Shrug': { name: "shrug", fi: 'Olankohautus' },
    'Namaste': { name: "namaste" }
  },

  // Preset animations
  animations: {
    'Walking': { url: './animations/walking.fbx', fi: 'Kävely' }
  },

  // Impulse responses
  impulses: {
    'Room': { url: './audio/ir-room.m4a', fi: 'Huone' },
    'Basement': { url: './audio/ir-basement.m4a', fi: 'Kellari' },
    'Forest': { url: './audio/ir-forest.m4a', fi: 'Metsä' },
    'Church': { url: './audio/ir-church.m4a', fi: 'Kirkko' }
  },

  // Background ambient sounds/music
  music: {
    'Murmur': { url: './audio/murmur.mp3', fi: 'Puheensorina'}
  }

};
