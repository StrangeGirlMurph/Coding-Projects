using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI : MonoBehaviour
{
    public Text infoText;
    float acceleration;
    int angle;
    GameObject rod;
    SinglePendulum script;

    void Start()
    {
        rod = GameObject.Find("Pendulum");
        script = rod.GetComponent<SinglePendulum>();
    }

    void Update()
    {
        acceleration = script.gravitationalAcceleration;
        angle = (int)(script.angleDeg);
        infoText.text = $"angle: {angle} \ng: {acceleration}";
    }
}
