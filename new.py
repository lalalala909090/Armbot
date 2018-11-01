#include <Servo.h> //调用舵机函数库
//定义舵机连接的arduino接口
int pin[7]={0,8,9,10,12,7,11};
//定义初始角度,0不使用
int Origin[7]={0,94,17,52,82,33,102};
//定义新位置
int NewPos[7]={0,94,17,52,82,33,102};
//标准时间间隔
int timeInterval=5000;
int ratio=250;

class Sweeper
{
  Servo myservo;//定义舵机
  int ServoNumber;//舵机编号
  int pos;//位置
  int increment=1;//每次增减角度
  int updateInterval=timeInterval/ratio;//更新的时间间隔
  unsigned long lastUpdate;//上次更新时间，与millis（）比较

public:
  /*Sweeper()
  {
    //updateInterval=interval;
    increment=1;
    //ServoNumber=number;
  }*/
  void OriginateServoNumber(int number)
  {
    ServoNumber=number;
  }
  //根据servoNumber Attach
  void Attach()
  {
    myservo.attach(pin[ServoNumber]);
  }
  //更新角度，mod 1：+，-1：-，0：不变,2：pos赋值，到达pos
  void Update(int mod,int ToPosition=0,int multiple=0)//mod，若mod=2到达的角度值，间隔时间的倍数值，比如0.5倍是一半的标准时间间隔
  {
    if((millis()-lastUpdate)>updateInterval*multiple)//time to update
    {
      lastUpdate=millis();//更新lastUpdate
      //mod为0则加。mod为-1则减
      if (mod==1)
      {
        pos+=increment;
        if(pos>180)
          pos=180;
      }
      else if(mod==-1)
      {
        pos-=increment;
        if(pos<0)
          pos=0;
      }
      else if (mod==2)
        pos=ToPosition;

      myservo.write(pos);
      //Serial.print("pos:    "+String(pos));
    }
  }
  //读取舵机角度值，断电重新开始一般均为93
  int Read()
  {
    return myservo.read();
  }
  int AngleChange()
  {
    return NewPos[ServoNumber]-myservo.read();
  }
};
/*Sweeper myservo1(timeInterval/ratio,1);
Sweeper myservo2(timeInterval/ratio,2);
Sweeper myservo3(timeInterval/ratio,3);
Sweeper myservo4(timeInterval/ratio,4);
Sweeper myservo5(timeInterval/ratio,5);
Sweeper myservo6(timeInterval/ratio,6);*/

Sweeper myservo[7];
//舵机转到卡死位置
void AllMovToExtreme()
{
  for (int i=180;i>=0;i--)
  {
    for(int n=1;n<=6;n++)
      myservo[n].Update(2,i);

    /*myservo1.Update(2,i);
    myservo2.Update(2,i);
    myservo3.Update(2,i);
    myservo4.Update(2,i);
    myservo5.Update(2,i);
    myservo6.Update(2,i);*/
    delay(timeInterval/ratio+1);
  }
}
void AllMovToOrigin()
{
  int pos=0;
  //只要有一个舵机没有到初始位置就始终循环
  while(pos<=Origin[1]||pos<=Origin[2]||pos<=Origin[3]||pos<=Origin[4]||pos<=Origin[5]||pos<=Origin[6])
  {
    /*if(pos<=Origin[1])
      myservo1.Update(2,pos);
    if(pos<=Origin[2])
      myservo2.Update(2,pos);
    if(pos<=Origin[3])
      myservo3.Update(2,pos);
    if(pos<=Origin[4])
      myservo4.Update(2,pos);
    if(pos<=Origin[5])
      myservo5.Update(2,pos);
    if(pos<=Origin[6])
      myservo6.Update(2,pos);*/
    for(int n=1;n<=6;n++)
    {
      if(pos<=Origin[n])
        myservo[n].Update(2,pos);
    }
    pos++;
    delay(timeInterval/ratio+1);
  }
}
void getNewPos()
{
  String small;
  //定义字符数组和字符串
  char getAngle[20]="";
  String Angle;
  Angle="";
  Serial.readBytes(getAngle,19);//读取传输的数据
  for (int j=0;j<=19;j++)
  {
    Angle=Angle+getAngle[j];
    Angle=Angle.substring(0,19);//去除可能的多余字符，如/n
  }

  //if(Angle.length()!=0&&Serial.available()>0)
  if(Angle.length()!=0)
  {
    Serial.print("Angle:");
    Serial.println(Angle);
    for (int i=1;i<=6;i++)
    {
      //输入新的角度值
      small=Angle.substring(3*i-3,3*i);
      NewPos[i]=small.toInt();
    }
  }
}
//主程序---------------------------------------------------

void setup()
{
  Serial.begin(9600);
  //连接舵机到端口

  for (int n=1;n<=6;n++)
  {
    myservo[n].OriginateServoNumber(n);
    myservo[n].Attach();
  }
/*  myservo1.Attach();
  myservo2.Attach();
  myservo3.Attach();
  myservo4.Attach();
  myservo5.Attach();
  myservo6.Attach();*/
  AllMovToExtreme();//统一转到极值
  AllMovToOrigin();//归位至初始位置
  int NewPos[7]={0,94,17,52,82,33,102};
  Serial.println("");
  Serial.println("");
  delay(timeInterval);
}
void loop()
{

  if(Serial.available()>0)
    getNewPos();

  for (int n=1;n<=6;n++)
  {
    Serial.print(NewPos[n]);
    //Serial.print(myservo[n].AngleChange());
    if(myservo[n].AngleChange()>0)
      myservo[n].Update(1,0,1/myservo[n].AngleChange());//若AngleChange>0，则角度值增加到要求值
    else if(myservo[n].AngleChange()<0)
      myservo[n].Update(-1,0,1/myservo[n].AngleChange());//若AngleChange<0，则角度值减小到要求值
    else
      myservo[n].Update(2,NewPos[n]);//若AngleChange=0，则保持位置
  }

  Serial.println("");

}
