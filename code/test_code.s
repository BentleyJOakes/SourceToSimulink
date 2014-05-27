	.file	"test_code.c"
	.text
	.align 2
.globl _Z11Const1_stepv
	.type	_Z11Const1_stepv, @function
_Z11Const1_stepv:
.LFB2:
	pushq	%rbp
.LCFI0:
	movq	%rsp, %rbp
.LCFI1:
	movss	Gain_Gain(%rip), %xmm1
	movss	Constant_Value(%rip), %xmm0
	mulss	%xmm1, %xmm0
	movss	%xmm0, out(%rip)
	movss	out(%rip), %xmm1
	movss	Constant1_Value(%rip), %xmm0
	mulss	%xmm1, %xmm0
	movss	%xmm0, out(%rip)
	movss	out(%rip), %xmm1
	movss	Const1_U(%rip), %xmm0
	addss	%xmm1, %xmm0
	movss	%xmm0, out(%rip)
	leave
	ret
.LFE2:
	.size	_Z11Const1_stepv, .-_Z11Const1_stepv
.globl __gxx_personality_v0
	.align 2
.globl main
	.type	main, @function
main:
.LFB3:
	pushq	%rbp
.LCFI2:
	movq	%rsp, %rbp
.LCFI3:
	movl	$0, %eax
	leave
	ret
.LFE3:
	.size	main, .-main
.globl Gain_Gain
	.data
	.align 4
	.type	Gain_Gain, @object
	.size	Gain_Gain, 4
Gain_Gain:
	.long	1084227584
.globl Constant_Value
	.align 4
	.type	Constant_Value, @object
	.size	Constant_Value, 4
Constant_Value:
	.long	1095027917
.globl Constant1_Value
	.align 4
	.type	Constant1_Value, @object
	.size	Constant1_Value, 4
Constant1_Value:
	.long	1107951616
.globl Const1_U
	.align 4
	.type	Const1_U, @object
	.size	Const1_U, 4
Const1_U:
	.long	1093035622
.globl out
	.bss
	.align 4
	.type	out, @object
	.size	out, 4
out:
	.zero	4
	.section	.eh_frame,"a",@progbits
.Lframe1:
	.long	.LECIE1-.LSCIE1
.LSCIE1:
	.long	0x0
	.byte	0x1
	.string	"zPR"
	.uleb128 0x1
	.sleb128 -8
	.byte	0x10
	.uleb128 0x6
	.byte	0x3
	.long	__gxx_personality_v0
	.byte	0x3
	.byte	0xc
	.uleb128 0x7
	.uleb128 0x8
	.byte	0x90
	.uleb128 0x1
	.align 8
.LECIE1:
.LSFDE1:
	.long	.LEFDE1-.LASFDE1
.LASFDE1:
	.long	.LASFDE1-.Lframe1
	.long	.LFB2
	.long	.LFE2-.LFB2
	.uleb128 0x0
	.byte	0x4
	.long	.LCFI0-.LFB2
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI1-.LCFI0
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE1:
.LSFDE3:
	.long	.LEFDE3-.LASFDE3
.LASFDE3:
	.long	.LASFDE3-.Lframe1
	.long	.LFB3
	.long	.LFE3-.LFB3
	.uleb128 0x0
	.byte	0x4
	.long	.LCFI2-.LFB3
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI3-.LCFI2
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE3:
	.ident	"GCC: (GNU) 4.2.1 (gccxml.org)"
	.section	.note.GNU-stack,"",@progbits
