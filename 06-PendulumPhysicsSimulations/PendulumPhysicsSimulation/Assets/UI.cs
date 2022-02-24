using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI : MonoBehaviour
{
    public Text gText;
    float g;
    int angle;
    GameObject rod;
    Pendulum script;

    // Start is called before the first frame update
    void Start()
    {
        rod = GameObject.Find("Pendulum");
        script = rod.GetComponent<Pendulum>();
    }

    // Update is called once per frame
    void Update()
    {
        g = script.g;
        angle = (int)(script.angleDeg);
        gText.text = $"angle: {angle} \ng: {g}";
    }
}
