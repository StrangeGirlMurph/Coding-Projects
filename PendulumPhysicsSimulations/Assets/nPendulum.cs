using UnityEngine;
using System;

public class nPendulum : MonoBehaviour
{
    public uint pendulumOrder = 1;
    public float gravitationalAcceleration = 9.81f;
    public float resistance = 0.01f; // 0 equals no friction
    public int repetitionsPerFrame = 100;


    Action<Piece[], float> calcAccelAndUpdate;

    void Awake()
    {
        SetN(pendulumOrder);
    }

    void SetN(uint n)
    {
        pendulumOrder = n;

        switch (n)
        {
            case 1:
                calcAccelAndUpdate = SingleAccel;
                break;
            case 2:
                calcAccelAndUpdate = DoubleAccel;
                break;
            default:
                calcAccelAndUpdate = NAccel;
                break;
        }
    }

    void FixedUpdate()
    {
        float fractionDeltatime = Time.fixedDeltaTime / repetitionsPerFrame;

        Piece[] pieces = gameObject.GetComponentsInChildren<Piece>();
        Vector2 incoming = Vector2.zero;

        for (double i = 0; i <= repetitionsPerFrame; i++)
        {
            calcAccelAndUpdate(pieces, fractionDeltatime);
        }
    }

    void SingleAccel(Piece[] piece, float time)
    {
        piece[0].angleA = -resistance * piece[0].angleV - (gravitationalAcceleration / piece[0].length) * Math.Sin(piece[0].angle);
        piece[0].UpdateAngle(time);
    }

    void DoubleAccel(Piece[] pieces, float time)
    {
        double g = gravitationalAcceleration;
        double m1 = pieces[0].mass;
        double m2 = pieces[1].mass;
        double l1 = pieces[0].length;
        double l2 = pieces[1].length;
        double a1 = pieces[0].angle;
        double a2 = pieces[1].angle;
        double v1 = pieces[0].angleV;
        double v2 = pieces[1].angleV;
        double sumMass = 2 * m1 + m2;
        double subAngle = a1 - a2;

        pieces[0].angleA = (-g * sumMass * sin(a1) - m2 * g * sin(a1 - 2 * a2) - 2 * sin(subAngle) * m2 * (Math.Pow(v2, 2) * l2 + Math.Pow(v1, 2) * l1 * cos(subAngle))) / (l1 * (sumMass - m2 * cos(2 * subAngle)));

        pieces[1].angleA = (2 * sin(subAngle) * (Math.Pow(v1, 2) * l1 * (m1 + m2) + g * (m1 + m2) * cos(a1) + Math.Pow(v2, 2) * l2 * m2 * cos(subAngle))) / (l1 * (sumMass - m2 * cos(2 * subAngle)));


        pieces[0].UpdateAngle(time);
        pieces[1].transform.position = pieces[0].transform.GetChild(1).transform.position;
        pieces[1].UpdateAngle(time);

    }

    void NAccel(Piece[] pieces, float time)
    {

    }

    double sin(double a)
    {
        return Math.Sin(a);
    }
    double cos(double a)
    {
        return Math.Cos(a);
    }
}
