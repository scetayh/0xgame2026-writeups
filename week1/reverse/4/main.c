#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define LRESULT int64_t
#define __fastcall
#define HWND void
#define UINT unsigned int
#define WPARAM uint64_t
#define LPARAM int64_t
#define __int64 long long
#define _QWORD uint64_t
#define _BYTE unsigned char
#define __int8 char

char aShedalight[10] = "Shedalight";

__int64 __fastcall sub_403700(__int64 a1, __int64 a2) { return 8 * a2 + a1; }

__int64 __fastcall sub_403730(__int64 a1, __int64 a2) {
    return sub_403700(a1, a2);
}

__int64 __fastcall sub_40184D(unsigned int *a1) {
    *a1 ^= *a1 << 13;
    *a1 ^= *a1 >> 17;
    *a1 ^= 32 * *a1;
    return *a1;
}

__int64 sub_4017EF(unsigned __int64 i, unsigned int v2) {
    // unsigned __int64 i; // [rsp+0h] [rbp-10h]
    // unsigned int v2;    // [rsp+Ch] [rbp-4h]

    v2 = -2128831035;
    for (i = 0; i <= 9; ++i)
        v2 = 16777619 * ((unsigned __int8)aShedalight[i] ^ v2);
    if (v2 != 0)
        return v2;
    else
        return 2738958700LL;
}

__int64 __fastcall sub_401550(__int64 a1, __int64 a2, unsigned __int64 a3) {
    __int64 result;     // rax
    unsigned __int8 v4; // [rsp+7h] [rbp-19h]
    unsigned __int64 j; // [rsp+8h] [rbp-18h]
    unsigned __int8 v6; // [rsp+17h] [rbp-9h]
    unsigned __int64 i; // [rsp+18h] [rbp-8h]

    for (i = 0; i <= 0xFF; ++i) {
        result = a1 + i;
        *(_BYTE *)(a1 + i) = i;
    }
    v6 = 0;
    for (j = 0; j <= 0xFF; ++j) {
        v6 += *(_BYTE *)(a1 + j) + *(_BYTE *)(j % a3 + a2);
        v4 = *(_BYTE *)(a1 + j);
        *(_BYTE *)(a1 + j) = *(_BYTE *)(a1 + v6);
        result = v4;
        *(_BYTE *)(v6 + a1) = v4;
    }
    return result;
}

unsigned char unk_405090[] = {
    0x32, 0xBA, 0x6C, 0x55, 0x7E, 0xCB, 0x91, 0x21, 0x58, 0x73, 0x01, 0x23,
    0xD9, 0xD0, 0x32, 0x54, 0x9C, 0xFA, 0x57, 0x00, 0x29, 0x3F, 0xE8, 0x31,
    0x75, 0xEF, 0x54, 0x29, 0x77, 0x59, 0x4F, 0x55, 0x20, 0x47, 0x4F, 0x54,
    0x20, 0x49, 0x54, 0x21, 0x21, 0x21, 0x0D, 0x0A, 0x00, 0x00, 0x00, 0x00};

unsigned char real_key[10] = "0xGame2025";

struct {
    unsigned char *ciphertext;   // +0
    unsigned __int64 length;     // +8
    unsigned char *key;          // +16
    unsigned __int64 key_length; // +24
    unsigned __int64 extra;      // +32
} off_405120 = {unk_405090, 29, real_key, 10, 0};

/*_UNKNOWN*/ unsigned char **sub_401768() {
    //   if ( IsDebuggerPresent() )
    //     return &off_4050C0;
    //   else
    return (unsigned char **)&off_405120;
}

unsigned __int64 __fastcall
sub_401620(/*__int64 */ char *a1, unsigned __int64 a2, __int64 a3, __int64 a4) {
    unsigned __int64 result; // rax
    _BYTE v5[270];           // [rsp+20h] [rbp-60h] BYREF
    char v6;                 // [rsp+12Eh] [rbp+AEh]
    char v7;                 // [rsp+12Fh] [rbp+AFh]
    unsigned __int64 i;      // [rsp+130h] [rbp+B0h]
    unsigned __int8 v9;      // [rsp+13Eh] [rbp+BEh]
    unsigned __int8 v10;     // [rsp+13Fh] [rbp+BFh]

    sub_401550((intptr_t)v5, a3, a4);
    v10 = 0;
    v9 = 0;
    for (i = 0;; ++i) {
        result = i;
        if (i >= a2)
            break;
        v9 += v5[++v10];
        v7 = v5[v10];
        v5[v10] = v5[v9];
        v5[v9] = v7;
        v6 = v5[(unsigned __int8)(v5[v10] + v5[v9])];
        *(_BYTE *)(a1 + i) ^= v6;
    }
    return result;
}

void __fastcall sub_4018A2(/*__int64 */ _BYTE *a1, unsigned __int64 a2) {
    unsigned __int64 v2;  // rax
    unsigned int v3;      // eax
    unsigned __int64 v4;  // rbx
    unsigned __int64 v5;  // rax
    int v6;               // [rsp+2Ch] [rbp-54h] BYREF
    _BYTE v7[263];        // [rsp+30h] [rbp-50h] BYREF
    char v8;              // [rsp+137h] [rbp+B7h]
    __int64 v9;           // [rsp+138h] [rbp+B8h]
    __int64 v10;          // [rsp+140h] [rbp+C0h]
    unsigned __int64 v11; // [rsp+148h] [rbp+C8h]
    unsigned __int64 v12; // [rsp+150h] [rbp+D0h]
    unsigned __int64 i;   // [rsp+158h] [rbp+D8h]

    if (a2 > 1) {
        memset(v7, 0, 0xF8u);
        v11 = a2 - 1;
        v6 = sub_4017EF(0, (intptr_t)v7);
        for (i = a2;; *(_QWORD *)sub_403730((intptr_t)v7, a2 - i - 1) = v4) {
            v2 = i--;
            if (v2 <= 1)
                break;
            v3 = sub_40184D(&v6);
            v4 = v3 % (i + 1);
        }
        v12 = v11;
        while (1) {
            v5 = v12--;
            if (v5 == 0)
                break;
            v10 = a2 - v12 - 1;
            v9 = *(_QWORD *)sub_403730((intptr_t)v7, v12);
            v8 = *(_BYTE *)(a1 + v10);
            *(_BYTE *)(a1 + v10) = *(_BYTE *)(a1 + v9);
            *(_BYTE *)(v9 + a1) = v8;
        }
    }
}

LRESULT __fastcall
sub_401B4B(/*HWND a1, */ UINT a2 /*, WPARAM a3, LPARAM a4*/) {
    char Source[/*8*/ 256] = {0}; // [rsp+30h] [rbp-50h] BYREF
    __int64 v6;             // [rsp+38h] [rbp-48h]
    __int64 v7;             // [rsp+40h] [rbp-40h]
    __int64 v8;             // [rsp+48h] [rbp-38h]
    // struct tagPAINTSTRUCT Paint; // [rsp+50h] [rbp-30h] BYREF
    char Destination[128]; // [rsp+A0h] [rbp+20h] BYREF
    // struct tagRECT Rect;         // [rsp+120h] [rbp+A0h] BYREF
    __int64 v12; // [rsp+130h] [rbp+B0h]
                 // HDC hdc;                     // [rsp+138h] [rbp+B8h]

    // if (a2 == 2) {
    //     PostQuitMessage(nExitCode : 0);
    //     return 0;
    // } else if (a2 == 15) {
    // memset(&Paint, 0, sizeof(Paint));
    // hdc = BeginPaint(hWnd : a1, lpPaint : &Paint);
    v12 = (intptr_t)sub_401768();
    *(_QWORD *)Source = 0;
    v6 = 0;
    v7 = 0;
    v8 = 0;
    memcpy(Source, *(const void **)v12, *(_QWORD *)(v12 + 8));
    sub_4018A2(Source, *(_QWORD *)(v12 + 8));
    sub_401620(Source, *(_QWORD *)(v12 + 8), *(_QWORD *)(v12 + 16),
               *(_QWORD *)(v12 + 24));
    memset(Destination, 0, sizeof(Destination));
    strcpy(Destination, "Your flag is ");
    strcat(Destination, Source);

    printf("%s\n", Destination);

    // *(_QWORD *)&Rect.left = 0;
    // *(_QWORD *)&Rect.right = 0;
    // GetClientRect(hWnd : a1, lpRect : &Rect);
    // DrawTextA(hdc, lpchText : Destination, cchText : -1, lprc : &Rect,
    //           format : 0x25u);
    // sub_401A43(*(_QWORD *)(v12 + 32), Source);
    // sub_402060(Source, 32);
    // EndPaint(hWnd : a1, lpPaint : &Paint);
    return 0;
    // } else {
    //     return DefWindowProcA(hWnd : a1, Msg : a2, wParam : a3, lParam : a4);
    // }
}

int main() { return sub_401B4B(15); }